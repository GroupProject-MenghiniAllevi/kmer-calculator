import multiprocessing
import os
from multiprocessing import Lock, Process
from it.unicam.cs.groupproject.kmer.Gerbil.DefaultGerbilUtils import DefaultGerbilUtils
from it.unicam.cs.groupproject.kmer.Gerbil.Gerbil import Gerbil
from it.unicam.cs.groupproject.kmer.Gerbil.SuperKmerReader import SuperKmerReader
from it.unicam.cs.groupproject.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from it.unicam.cs.groupproject.kmer.Utils.DefaultKmerReader import DefaultKmerReader
from it.unicam.cs.groupproject.kmer.Utils.OutputWriter import OutputWriter


class DefaultGerbil(Gerbil):
    __partition_path = ""

    __input_path = ""

    __m = 0
    __k = 0
    __output_path = ""
    __lock = Lock()

    def __init__(self, input_path, partition_path, out_path, k, m) -> None:
        self.__partition_path = partition_path
        self.__input_path = input_path
        self.__m = m
        self.__k = k
        self.__output_path = out_path

    def process(self):
        self.start_first_phase_process()
        out_file = None
        try:
            out_file = open(self.__output_path, "x")
            out_file.close()
        except FileExistsError:
            out_file = open(self.__output_path, "w+")
            out_file.truncate()
            out_file.seek(0)
            out_file.close()
        self.start_second_phase_process()

    def start_first_phase_process(self):
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        process_list = list()
        self.__lock = Lock()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            process = Process(target=self.process_read_and_write_minimizer(file_fullpath))
            process.start()
            process_list.append(process)
        for p in process_list:
            p.join()

    def process_read_and_write_minimizer(self, file_fullpath):
        self.__lock.acquire()
        kmer_reader = DefaultKmerReader()
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(file_fullpath)
        size = (kmer_reader.get_file_lenght() - self.__k) + 1
        minimizer_ith = 0
        gerbil_utils = DefaultGerbilUtils(self.__k, self.__m)
        minimizer = b""
        minimizer_max = self.__k - self.__m + 1
        kmer_list = list()
        while kmer_reader.has_next(size):
            kmer = kmer_reader.read_next_kmer()
            kmer_list.append(kmer)
            if minimizer_ith == 0:
                minimizer = gerbil_utils.get_minimizers_from_kmer(kmer)
            if minimizer_ith == minimizer_max - 1:
                gerbil_utils.find_super_kmer_and_write(kmer_list, self.__lock, minimizer, self.__partition_path)
                minimizer_ith = 0
                kmer_list.clear()
                gerbil_utils = DefaultGerbilUtils(self.__k, self.__m)
            else:
                minimizer_ith += 1
        kmer_reader.close_file()
        if len(kmer_list):
            gerbil_utils.find_super_kmer_and_write(kmer_list, self.__lock, minimizer, self.__partition_path)
        self.__lock.release()

    def start_second_phase_process(self):
        process_list = list()
        dh = DefaultDirectoryHandler(self.__partition_path)
        file_list = dh.get_all_files_names()
        self.__lock = Lock()
        concurrency = 4
        total_task_num = len(file_list)
        sema = multiprocessing.Semaphore(concurrency)
        for file in range(total_task_num):
            p = Process(target=self.read_from_partition_and_counting, args=(file_list[file],sema))
            process_list.append(p)
            p.start()

        for p in process_list:
            p.join()

    def read_from_partition_and_counting(self, file_partition_path,sema):
        sema.acquire()
        file_without_ext = file_partition_path.replace('.bin', '')
        minimizer = os.path.basename(os.path.normpath(file_without_ext))
        file_full_path = os.path.join(self.__partition_path, file_partition_path)
        super_kmer_reader = SuperKmerReader(file_full_path, self.__k, minimizer)
        size = super_kmer_reader.get_file_lenght()
        gerbil_util = DefaultGerbilUtils(self.__k, self.__m)
        hash_table_size = 20
        index_hash_t = 0
        hash_table = gerbil_util.get_empty_hash_map()

        while super_kmer_reader.has_next(size-1):
            kmer = super_kmer_reader.read_next_kmer()
            if kmer in hash_table:
                hash_table[kmer] = hash_table[kmer] + 1
            else:
                hash_table[kmer] = 1
            index_hash_t += 1
            if index_hash_t - 1 > hash_table_size:
                output_writer = OutputWriter()
                output_writer.write_to_output(self.__output_path, hash_table)
                hash_table = gerbil_util.get_empty_hash_map()
        if len(hash_table)>0:
            output_writer = OutputWriter()
            output_writer.write_to_output(self.__output_path, hash_table)
            print(self.__output_path)
        sema.release()
