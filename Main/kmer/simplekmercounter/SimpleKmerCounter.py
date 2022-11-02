import os

from Main.kmer.Utils.Reader.DbNhKmerReader import DefaultDbNhReader
from Main.kmer.Utils.Reader.ExcelMoleculeReader import ExcelMoleculeReader, get_default_path
from Main.kmer.Utils.Writer.OutputWriter import OutputWriter


class SimpleKmerCounter:
    __input_path = ""
    __k = -1
    __reader = DefaultDbNhReader()
    __ht = dict()
    __file_list = list()
    __molecules_name = dict()

    def __init__(self, input_path, k):
        self.__k = k
        self.__input_path = input_path
        self.__file_list = [x for x in os.listdir(input_path) if x.endswith(".db")]
        self.detect_molecule_name_from_input()

    def process(self,output_path):
        for file in self.__file_list:
            self.__reader = DefaultDbNhReader()
            self.__reader.set_path(os.path.join(self.__input_path, file))
            self.__reader.set_kmer_lenght(k=self.__k)
            size = self.__reader.get_file_lenght()
            i = 0
            while self.__reader.has_next(size):
                kmer = self.get_next_kmer()
                if kmer in self.__ht:
                    self.__ht[kmer] = self.__ht[kmer] + 1
                else:
                    self.__ht[kmer] = 1
                i += 1
            self.__ht = self.__sort_dictionary(self.__ht)
            output_writer = OutputWriter(self.__molecules_name[file], output_path)
            output_writer.write_to_output(self.__ht)
            self.__ht.clear()
            self.__reader.close_file()

    def detect_molecule_name_from_input(self):
        excel_files_path = get_default_path()
        l = [f for f in os.listdir(excel_files_path) if os.path.isfile(os.path.join(excel_files_path, f)) and f.endswith(".xlsx")]
        excel_file_list = [v for v in l if v.endswith(".xlsx")]
        check_nH = False
        if not self.__file_list[0].find("_nH.db") == -1:
            check_nH = True
        clean_file_list = [v.replace("_nH.db", ".db") for v in self.__file_list]
        for excel_file in excel_file_list:
            path = os.path.join(excel_files_path, excel_file)
            reader = ExcelMoleculeReader(path=path)
            reader.extract_list_of_all_sheet()
            reader.extract_all_molecule_name()
            d = reader.get_molecules()
            d = self.__add_db_to_filename(d)
            for key in d:
                if key in clean_file_list:
                    s = key
                    s_index = len(s) - 3
                    if check_nH:
                        s = s[:s_index] + "_nH" + s[s_index:]
                    self.__molecules_name[s] = d[key]
        return self.__molecules_name

    def __sort_dictionary(self, ht):
        s = dict(sorted(ht.items()))
        return s

    def  get_next_kmer(self):
        return self.__reader.read_next_kmer()

    def __add_db_to_filename(self, d):
        x = dict()
        for key in d:
            s = key + ".db"
            x[s] = d[key]
        return x
