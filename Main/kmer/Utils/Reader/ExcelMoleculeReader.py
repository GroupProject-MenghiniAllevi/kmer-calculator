import os

import pandas as pd


def get_default_path():
    act_path = os.path.abspath(__file__)
    read_path = os.path.dirname(act_path)
    utils_path = os.path.dirname(read_path)
    kmer_path = os.path.dirname(utils_path)
    main_path = os.path.dirname(kmer_path)
    root = os.path.dirname(main_path)
    resource_path = os.path.join(root, "resource")
    return os.path.join(resource_path, "ExcelFile")


class ExcelMoleculeReader:
    __path = ""
    __df = None
    __sheet_list = list()
    __molecules = dict()
    __excel_files = ("Archaea.xlsx", "Bacteria.xlsx", "Eukaryota.xlsx")
    __mode = True

    def __init__(self, path):
        self.__path = path


    def extract_sheet(self, sheet_name):
        xls = pd.ExcelFile(self.__path)
        self.__df = pd.read_excel(xls, sheet_name)
        return self.__df

    def get_name_of_molecule(self, benchmark_id):
        #print(benchmark_id.encode('utf-8'), benchmark_id == "CRW_16S_B_C_40 ")
        sub_df = self.__df.loc[self.__df['Benchmark ID'] == benchmark_id]
        name = sub_df.iloc[0]['Organisms']
        name = name.replace('\xa0', '')
        name = name.replace("\n", "")
        name = name.replace("\r", "")
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
            if sheet_name == "16S":
                print("CRW_16S_B_C_40 " in file_list)
            for bench_id in file_list:
                if bench_id == "CRW_16S_B_C_40 ":
                    print("Ciaooo")
                name = self.get_name_of_molecule(bench_id)
                bench_id = bench_id.replace(" ", "")
                bench_id = bench_id.replace("\n", "")
                bench_id = bench_id.replace("\r", "")
                self.__molecules[bench_id] = name

    def get_molecules(self):
        return self.__molecules

