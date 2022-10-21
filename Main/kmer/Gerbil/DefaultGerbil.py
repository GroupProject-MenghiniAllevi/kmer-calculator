import os
import shutil
from multiprocessing import Lock, Process
from Main.kmer.Utils.minimizer.DefaultMinimizerHandler import DefaultMinimizerHandler
from Main.kmer.Gerbil.Gerbil import Gerbil
from Main.kmer.Utils.Reader.SuperKmerReader import SuperKmerReader
from Main.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.Reader.DefaultKmerReader import DefaultKmerReader
from Main.kmer.Utils.Writer.OutputWriter import OutputWriter


class DefaultGerbil(Gerbil):
    __partition_path = ""

    __input_path = ""
    __molecule_list = dict()
    __m = 0
    __k = 0
    __output_path = ""
    __lock = Lock()
    __partition_path_list = list()
    __super_kmer_length = 0

    def __init__(self, input_path, partition_path, out_path, k, m) -> None:
        self.__partition_path = partition_path
        self.__input_path = input_path
        self.__m = m
        self.__k = k
        self.__super_kmer_length = k - m + 1
        self.__output_path = out_path

    def process(self):
        self.start_first_phase_process()
        self.check_molecule_lists()
        self.start_second_phase_process()
        self.__delete_all_partitions()

    def check_molecule_lists(self):
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            reader = DefaultKmerReader()
            reader.set_path(file_fullpath)
            reader.set_kmer_lenght(self.__k)
            name = reader.get_file_name()
            reader.close_file()
            name = name.strip()
            self.__molecule_list[file] = name
        return self.__molecule_list

    def start_first_phase_process(self):
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        process_list = list()
        self.__lock = Lock()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            reader = DefaultKmerReader()
            reader.set_path(file_fullpath)
            reader.set_kmer_lenght(self.__k)
            name = reader.get_file_name()
            reader.close_file()
            name = name.strip()
            partition_file_path = self.create_partition(name)
            self.__partition_path_list.append(partition_file_path)
            p = Process(target=self.process_read_and_write_minimizer(file_fullpath, partition_file_path, name))
            p.start()
            process_list.append(p)
        for process in process_list:
            process.join()

    def create_partition(self, file):
        file_part = os.path.join(self.__partition_path, file)
        if not os.path.exists(file_part):
            os.mkdir(file_part)
        return file_part

    def process_read_and_write_minimizer(self, file_fullpath, partition_file_path, filename):
        self.__lock.acquire()
        min_ith = 0
        reader = DefaultKmerReader()
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
        for key in self.__molecule_list:
            name = self.__molecule_list[key]  # nome della molecola
            part_path = os.path.join(self.__partition_path,
                                     name)  # path della partizione che corrisponde al nome della molecola.
            dh = DefaultDirectoryHandler(part_path)
            file_list = dh.get_all_files_names()  # leggo tutti i file dentro la partizione.
            # print("file_name:",key," part_list:",part_path)
            for file in file_list:  # itero tutti i file dentro la partizione
                filepath = os.path.join(part_path, file)  # path del file nella partizione
                ht = self.read_from_partition_and_counting(filepath, self.__lock, name)
                writer = OutputWriter(filename=name, path=self.__output_path)
                ht = self.__sort_dictionary(ht)
                writer.write_to_output(ht)

    def read_from_partition_and_counting(self, partition_filepath, sema, molecule_name):
        sema.acquire()
        file_without_ext = partition_filepath.replace('.bin', '')
        minimizer = os.path.basename(os.path.normpath(file_without_ext))
        reader = SuperKmerReader(partition_filepath, self.__k, minimizer)
        size = reader.get_file_lenght()
        hash_table = dict()
        while reader.has_next(size - 1):
            kmer = reader.read_next_kmer()
            if kmer in hash_table:
                hash_table[kmer] = hash_table[kmer] + 1
            else:
                hash_table[kmer] = 1
        sema.release()
        return hash_table

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
