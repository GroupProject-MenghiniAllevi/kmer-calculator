import os.path
import shutil

from Main.kmer.KMC3.KMC3 import KMC3
from Main.kmer.Utils.Reader.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.MostSignificantRadixSort import MostSignificantRadixSort
from Main.kmer.Utils.Reader.DbNhKmerReader import FastaRnaReader
from Main.kmer.Utils.Reader.ExcelMoleculeReader import ExcelMoleculeReader,get_default_path
from Main.kmer.Utils.Reader.SuperKmerReader import SuperKmerReader
from Main.kmer.Utils.Writer.OutputWriter import OutputWriter
from Main.kmer.Utils.minimizer.DefaultMinimizerHandler import DefaultMinimizerHandler


class DefaultKMC3(KMC3):
    __input_path = ""
    __partition_path = ""
    __output_path = ""
    __k = 0
    __m = 0
    __input_file_list = list()
    __molecule_dict = dict()
    __partition_sub_dict = dict()

    def __init__(self, input_path, partition_path, output_path, k, m):
        self.__m = m
        self.__k = k
        self.__input_path = input_path
        self.__partition_path = partition_path
        self.__output_path = output_path

    def write_kmer_to_partition(self, partition_sub_path, input_file_path):
        reader = FastaRnaReader()
        reader.set_path(input_file_path)
        reader.set_kmer_lenght(self.__k)
        length = reader.get_file_lenght()
        min_ith = 0
        minimizer = ""
        kmer_list = list()
        mh = DefaultMinimizerHandler(self.__k, self.__m)
        super_kmer_size = self.__k - self.__m
        while reader.has_next(length):
            kmer = reader.read_next_kmer()
            if min_ith == 0 or minimizer == "":
                kmer_list.append(kmer)
                minimizer = mh.get_minimizers_from_kmer(kmer)
                min_ith += 1
            elif min_ith == super_kmer_size:
                kmer_list.append(kmer)
                mh.find_super_kmer_and_write(kmer_list, minimizer, partition_sub_path)
                minimizer = ""
                kmer_list.clear()
                min_ith = 0
            else:
                kmer_list.append(kmer)
                min_ith += 1
        if len(kmer_list) > 0:
            print(kmer_list)
            mh.find_super_kmer_and_write(kmer_list, minimizer, partition_sub_path)

    def read_skmer_and_print_to_output(self, filepart_path):
        part_name = os.path.basename(os.path.normpath(filepart_path))
        sorted_part = self.__get_file_list_from_part(filepart_path)
        for file in sorted_part:
            minimizer = os.path.basename(os.path.normpath(file))
            minimizer = minimizer.replace(".bin", "")
            reader = SuperKmerReader(file, self.__k, minimizer)
            size = reader.get_file_lenght()
            ht = dict()
            while reader.has_next(size - 1):
                kmer = reader.read_next_kmer()
                if kmer in ht:
                    ht[kmer] += 1
                else:
                    ht[kmer] = 1
                if len(ht) > 256:
                    self.__write_kmer_count(part_name, ht)
                    ht.clear()
            if len(ht) > 0:
                self.__write_kmer_count(part_name, ht)
                ht.clear()

    def __write_kmer_count(self, file, ht):
        output_writer = OutputWriter(file, self.__output_path)
        output_writer.write_to_output(ht)
        output_writer.close_all_files()
        ht.clear()

    def process(self):
        self.__input_file_list = self.extract_file_list()
        self.create_partitions(self.__partition_path, self.__input_file_list)
        self.extract_molecule_name()
        for file in self.__input_file_list:
            input_file_path = os.path.join(self.__input_path, file)
            #print("Leggendo i k-mer del file "+file+"...")
            self.write_kmer_to_partition(self.__partition_sub_dict[file], input_file_path)
            print("Ricostruendo i k-mer e la loro frequenza del file "+file+"...")
            self.read_skmer_and_print_to_output(self.__partition_sub_dict[file])

    def extract_file_list(self):
        dh = DefaultDirectoryHandler(path=self.__input_path)
        l = dh.get_all_files_names()
        l.sort()
        return l

    def create_partitions(self, path, file_list):
        self.__input_file_list = file_list
        for file in self.__input_file_list:
            part_path = os.path.join(path, file)
            if not os.path.exists(part_path):
                os.mkdir(part_path)
            else:
                shutil.rmtree(part_path)
                os.mkdir(part_path)
            self.__partition_sub_dict[file] = part_path

    def extract_molecule_name(self):
        excel_files_path = get_default_path()
        l = [f for f in os.listdir(excel_files_path) if
             os.path.isfile(os.path.join(excel_files_path, f)) and f.endswith(".xlsx")]
        excel_file_list = [v for v in l if v.endswith(".xlsx")]
        check_nH = False
        if not self.__input_file_list[0].find("_nH.db") == -1:
            check_nH = True
        clean_file_list = [v.replace("_nH.db", ".db") for v in self.__input_file_list]
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
                    self.__molecule_dict[s] = d[key]

    def __get_file_list_from_part(self, filepart_path):
        partition_list = os.listdir(filepart_path)
        for i in range(len(partition_list)):
            partition_list[i] = partition_list[i].replace(".bin","")
        msd_radix_sort = MostSignificantRadixSort(partition_list)
        msd_radix_sort.sort()
        sorted_part = msd_radix_sort.get_list()
        # print(partition_list)
        # print(sorted_part)
        s = list()
        for file in sorted_part:
            s.append(os.path.join(filepart_path, file+".bin"))
        return s

    def __add_db_to_filename(self, d):
        x = dict()
        for key in d:
            s = key + ".db"
            x[s] = d[key]
        return x
