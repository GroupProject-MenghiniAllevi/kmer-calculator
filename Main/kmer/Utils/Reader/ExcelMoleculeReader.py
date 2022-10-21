import pandas as pd


class ExcelMoleculeReader:
    __path = ""
    __df = None
    __sheet_list = list()
    __molecules = dict()

    def __init__(self, path):
        self.__path = path

    def extract_sheet(self, sheet_name):
        xls = pd.ExcelFile(self.__path)
        self.__df = pd.read_excel(xls, sheet_name)
        return self.__df

    def get_name_of_molecule(self, benchmark_id):
        sub_df = self.__df.loc[self.__df['Benchmark ID'] == benchmark_id]
        name = sub_df.iloc[0]['Organisms']
        name = name.replace('\xa0', '')
        return name

    def extract_list_of_all_sheet(self):
        self.__sheet_list.clear()
        self.__df = pd.ExcelFile(self.__path)
        for sheet_name in self.__df.sheet_names:
            self.__sheet_list.append(sheet_name)

    def get_sheet_names(self):
        return self.__sheet_list

    def extract_all_molecule_name(self):
        for sheet_name in self.__sheet_list:
            self.extract_sheet(sheet_name)
            file_list = self.__df["Benchmark ID"]
            for bench_id in file_list:
                self.__molecules[bench_id] = self.get_name_of_molecule(bench_id)

    def get_molecules(self):
        return self.__molecules
