import os.path
from os.path import dirname
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import VarianceThreshold, SelectFromModel, RFE, \
    chi2, SelectPercentile
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from stability_selection import RandomizedLogisticRegression, StabilitySelection


class FSelector:
    __df = None
    __output_arr = []
    __columns_list = list()
    __selected_features = []
    __molecule_list = []
    __molecule_expected = {}
    __sheets = ("5S", "16S", "23S")

    def __init__(self, path, supervised: bool = False, search: str = ""):
        if len(path) <= 0:
            raise ValueError("Non è stato inserito nessun percorso...")
        else:
            if not os.path.exists(path):
                with open(path, "x") as file:
                    file.truncate()
                    file.close()
            columns_size = self.__detect_column_size(path)
            self.__df = pd.read_csv(path, skiprows=[0], usecols=range(1, columns_size + 1), header=None)
            #print(path)
            self.__detect_column_name(path)
            if supervised:
                self.__detect_molecule_expected(search)

    def apply_low_variance(self, threshold):
        sel = VarianceThreshold(threshold=threshold)
        arr = sel.fit_transform(X=self.__df)
        self.__selected_features = sel.get_support()
        self.__output_arr = arr

    def apply_L1_based(self):
        y = np.asarray(list(self.__molecule_expected.values()))
        lsvc = LinearSVC(C=0.1, penalty="l1", dual=False).fit(X=self.__df, y=y)
        model = SelectFromModel(lsvc, prefit=True)
        self.__output_arr = model.transform(X=self.__df)
        self.__selected_features = model.get_support()

    def apply_Sequential_features_selection(self):
        y = np.asarray(list(self.__molecule_expected.values()))
        svc = SVC(kernel="linear", C=1)
        rfe = RFE(estimator=svc)
        rfe.fit(self.__df, y)
        self.__selected_features = rfe.get_support()
        self.__output_arr = rfe.transform(X=self.__df)

    def write_to_output(self, output_path):
        l = list()
        l.append("id")
        c = 0
        for i in range(0, len(self.__selected_features)):
            if self.__selected_features[i]:
                l.append(self.__columns_list[i + 1])
                c += 1
        df = pd.DataFrame(columns=l)
        row = list()
        # print(len(self.__selected_features), len(self.__output_arr), len(self.__molecule_list))
        for i in range(len(self.__molecule_list)):
            row.append(self.__molecule_list[i])
            j = 0
            for value in self.__selected_features:
                if value:
                    row.append(self.__output_arr[i][j])
                    j += 1
            df.loc[len(df.index)] = row
            row = list()
        if not os.path.exists(output_path):
            with open(output_path, "x") as file:
                file.close()
        else:
            with open(output_path, "wb+") as file:
                file.close()
        df.to_csv(output_path, index=False)

    def __detect_column_size(self, path):
        readed_value = ""
        counter = 0
        self.__columns_list.append("id")
        with open(path, "rb") as file:
            while True:
                c = file.read(1)
                if not c or c == b"\n" or c == b"\r":
                    if not readed_value == 'id':
                        counter += 1
                        self.__columns_list.append(readed_value)
                    break
                elif c == b",":
                    if not readed_value == 'id':
                        counter += 1
                        self.__columns_list.append(readed_value)
                    readed_value = ""
                else:
                    readed_value += c.decode('utf-8')
            file.close()
        return counter

    def __detect_column_name(self, path):
        self.__molecule_list.clear()
        column = 0
        readed_value = ""
        with open(path, "rb") as file:
            file.readline()
            while True:
                c = file.read(1)
                if not c:
                    if column == 0 and not readed_value == "":
                        self.__molecule_list.append(readed_value)
                    break
                elif c == b",":
                    if column == 0 and not readed_value == "":
                        self.__molecule_list.append(readed_value)
                    column += 1
                    readed_value = ""
                elif c == b"\n" or c == b"\r":
                    if column == 0 and not readed_value == "":
                        self.__molecule_list.append(readed_value)
                    column = 0
                    readed_value = ""
                else:
                    readed_value += c.decode('utf-8')
            file.close()
            # print(self.__molecule_list)

    def __detect_molecule_expected(self,search):
        # print(self.__molecule_list)
        molecules_path = self.__get_molecules_path()
        sub_file_path = [name for name in os.listdir(molecules_path) if
                         os.path.isfile(os.path.join(molecules_path, name))]
        for file in sub_file_path:
            path = os.path.join(molecules_path, file)
            for s in self.__sheets:
                df = pd.read_excel(path, sheet_name=s)
                #print(len(self.__molecule_list))
                sep = "."
                l = [x.split(sep, 1)[0] for x in self.__molecule_list]
                # print(len(l))
                for mol in l:
                    if not mol in self.__molecule_expected:
                        v = df.loc[df['Benchmark ID'] == mol]
                        if not v.empty:
                            value = v.iloc[0][search]
                            value = value.replace('\xa0', '')
                            value = value.strip()
                            self.__molecule_expected[mol] = value
                        else:
                            m = mol + "\xa0"
                            v = df.loc[df['Benchmark ID'] == m]
                            if not v.empty:
                                value = v.iloc[0][search]
                                value = value.replace('\xa0', '')
                                value = value.strip()
                                self.__molecule_expected[mol] = value
                            else:
                                m = mol + " "
                                v = df.loc[df['Benchmark ID'] == m]
                                if not v.empty:
                                    value = v.iloc[0][search]
                                    value = value.replace('\xa0', '')
                                    value = value.strip()
                                    self.__molecule_expected[mol] = value
    def __get_molecules_path(self):
        root = dirname(dirname(dirname(os.path.abspath(__file__))))
        resource_path = os.path.join(root, "resource")
        return os.path.join(resource_path, "ExcelFile")

    def apply_recursive_tree(self):
        y = np.asarray(list(self.__molecule_expected.values()))
        clf = ExtraTreesClassifier(n_estimators=5)
        clf = clf.fit(self.__df, y)
        model = SelectFromModel(clf, prefit=True)
        self.__output_arr = model.transform(self.__df)
        self.__selected_features = model.get_support()

    def apply_chi2_test(self):
        y = np.asarray(list(self.__molecule_expected.values()))
        chi2_feat = SelectPercentile(chi2)
        self.__output_arr = chi2_feat.fit_transform(self.__df, y)
        self.__selected_features = chi2_feat.get_support()

    def rlr(self):
        y = np.asarray(list(self.__molecule_expected.values()))
        # y = self.__create_data_for_rlr(y)
        print("unique:",np.unique(y))
        estimator = RandomizedLogisticRegression()
        selector = StabilitySelection(base_estimator=estimator,n_jobs=1)
        self.__output_arr = selector.fit_transform(self.__df,y)
        self.__selected_features = selector.get_support()

    def __create_data_for_rlr(self,y):
        new_y = []
        different_label = [class_ for class_ in y if not class_ in y]
        different_label.sort()
        sub_arr_size = len(different_label)
        for data in y:
            sub_array = [0] * sub_arr_size
            for index in range(len(different_label)):
                if different_label[index] == data:
                    sub_array.append(1)
                else:
                    sub_array.append(0)
            new_y.append(sub_array)
        return new_y