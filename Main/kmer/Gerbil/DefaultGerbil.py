import os
import shutil
from multiprocessing import Lock, Process

from Main.kmer.Utils.Reader.DbNhKmerReader import DefaultDbNhReader
from Main.kmer.Utils.minimizer.DefaultMinimizerHandler import DefaultMinimizerHandler
from Main.kmer.Gerbil.Gerbil import Gerbil
from Main.kmer.Utils.Reader.SuperKmerReader import SuperKmerReader
from Main.kmer.Utils.Reader.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.Writer.OutputWriter import OutputWriter
from Main.kmer.Utils.Reader.ExcelMoleculeReader import ExcelMoleculeReader, get_default_path



class DefaultGerbil(Gerbil):
    __partition_path = ""
    __input_path = ""
    __molecules_name = dict()
    __m = 0
    __k = 0
    __output_path = ""
    __lock = Lock()
    __partition_path_list = list()
    __super_kmer_length = 0
    __file_list = []

    def __init__(self, input_path, partition_path, out_path, k, m) -> None:
        self.__partition_path = partition_path
        self.__input_path = input_path
        self.__m = m
        self.__k = k
        self.__super_kmer_length = k - m + 1
        self.__output_path = out_path
        dh = DefaultDirectoryHandler(input_path)
        self.__file_list = dh.get_all_files_names()

    def process(self):
        self.detect_molecule_name_from_input()
        self.check_molecule_lists()
        self.start_first_phase_process()
        self.start_second_phase_process()
        self.__delete_all_partitions()

    def check_molecule_lists(self):
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            reader = DefaultDbNhReader()
            reader.set_path(file_fullpath)
            reader.set_kmer_lenght(self.__k)
            reader.close_file()
        return self.__molecules_name

    def detect_molecule_name_from_input(self):
        default_path = get_default_path()
        l = [f for f in os.listdir(default_path) if os.path.isfile(os.path.join(default_path, f)) and f.endswith(".xlsx")]
        excel_file_list = [v for v in l if v.endswith(".xlsx")]
        check_nH = False
        if not self.__file_list[0].find("_nH.db") == -1:
            check_nH = True
        clean_file_list = [v.replace("_nH.db", ".db") for v in self.__file_list]
        for excel_file in excel_file_list:
            path = os.path.join(default_path, excel_file)
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

    def start_first_phase_process(self):
        print("iniziata la prima fase...")
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        process_list = list()
        self.__lock = Lock()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            reader = DefaultDbNhReader()
            reader.set_path(file_fullpath)
            reader.set_kmer_lenght(self.__k)
            reader.close_file()
            partition_file_path = self.create_partition(self.__molecules_name[file])
            self.__partition_path_list.append(partition_file_path)
            self.process_read_and_write_minimizer(file_fullpath, partition_file_path, self.__molecules_name[file])
            # p = Process(target=self.process_read_and_write_minimizer(file_fullpath, partition_file_path, self.__molecules_name[file]))
            # p.start()
            # process_list.append(p)
        for process in process_list:
            process.join()
        print("terminata la prima fase...")

    def create_partition(self, file):
        file_part = os.path.join(self.__partition_path, file)
        if not os.path.exists(file_part):
            os.mkdir(file_part)
        return file_part

    def __add_db_to_filename(self, d):
        x = dict()
        for key in d:
            s = key + ".db"
            x[s] = d[key]
        return x

    def process_read_and_write_minimizer(self, file_fullpath, partition_file_path, filename):
        self.__lock.acquire()
        min_ith = 0
        reader = DefaultDbNhReader()
        reader.set_path(file_fullpath)
        reader.set_kmer_lenght(self.__k)
        size = reader.get_file_lenght()
        minimizer = ""
        gerbil_utils = DefaultMinimizerHandler(self.__k, self.__m)
        kmer_list = list()
        while reader.has_next(size):
            kmer = reader.read_next_kmer()
            if min_ith == 0:
                minimizer = gerbil_utils.get_minimizers_from_kmer(kmer)
                min_ith += 1
                kmer_list.append(kmer)
            elif min_ith == self.__super_kmer_length - 1:
                kmer_list.append(kmer)
                gerbil_utils.find_super_kmer_and_write(kmer_list, minimizer, partition_file_path)
                min_ith = 0
                kmer_list.clear()
            else:
                min_ith += 1
                kmer_list.append(kmer)
        if len(kmer_list) > 0:
            gerbil_utils.find_super_kmer_and_write(kmer_list, minimizer, partition_file_path)
        self.__lock.release()

    def start_second_phase_process(self):
        print("iniziata la seconda fase...")
        for key in self.__molecules_name:
            name = self.__molecules_name[key]  # nome della molecola
            part_path = os.path.join(self.__partition_path,
                                     name)  # path della partizione che corrisponde al nome della molecola.
            file_list = os.listdir(part_path)  # leggo tutti i file dentro la partizione.
            for file in file_list:  # itero tutti i file dentro la partizione
                filepath = os.path.join(part_path, file)  # path del file nella partizione
                ht = self.read_from_partition_and_counting(filepath, self.__lock, name)
                writer = OutputWriter(filename=name, path=self.__output_path)
                ht = self.__sort_dictionary(ht)
                writer.write_to_output(ht)
        print("terminata la seconda fase...")
    def read_from_partition_and_counting(self, partition_filepath, sema, molecule_name):
        sema.acquire()
        file_without_ext = partition_filepath.replace('.bin', '')
        minimizer = os.path.basename(os.path.normpath(file_without_ext))
        reader = SuperKmerReader(partition_filepath, self.__k, minimizer)
        size = reader.get_file_lenght()
        d = dict()
        while reader.has_next(size - 1):
            kmer = reader.read_next_kmer()
            if kmer in d:
                d[kmer] = d[kmer] + 1
            else:
                d[kmer] = 1
        sema.release()
        return d

    def __get_partitions(self):
        l = os.listdir(self.__partition_path)
        return l

    def __delete_all_partitions(self):
        part_list = os.listdir(self.__partition_path)
        for path in part_list:
            p = os.path.join(self.__partition_path, path)
            shutil.rmtree(p)

    def __sort_dictionary(self, ht):
        s = dict(sorted(ht.items()))
        return s
