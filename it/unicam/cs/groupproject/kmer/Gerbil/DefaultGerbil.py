import os
from multiprocessing import Lock, Process
import pandas as pd
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo
from it.unicam.cs.groupproject.kmer.Gerbil.DefaultGerbilUtils import DefaultGerbilUtils
from it.unicam.cs.groupproject.kmer.Gerbil.Gerbil import Gerbil
from it.unicam.cs.groupproject.kmer.Gerbil.SuperKmerReader import SuperKmerReader
from it.unicam.cs.groupproject.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from it.unicam.cs.groupproject.kmer.Utils.DefaultKmerReader import DefaultKmerReader


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
        open(self.__output_path,"x")
        self.start_first_phase_process()

    def start_first_phase_process(self):
        dh = DefaultDirectoryHandler(self.__input_path)
        file_list = dh.get_all_files_names()
        process_list = list()
        for file in file_list:
            file_fullpath = os.path.join(self.__input_path, file)
            print(file_fullpath)
            p = Process(target=self.__process_read_and_write_minimizer, args=(file_fullpath,))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()

    def __process_read_and_write_minimizer(self, file_fullpath):
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
            if minimizer_ith == 0:
                minimizer = gerbil_utils.get_minimizers_from_kmer(kmer)
            elif minimizer_ith == minimizer_max - 1:
                gerbil_utils.find_super_kmer_and_write(kmer_list, self.__lock, minimizer)
                minimizer_ith = 0
            else:
                kmer_list.append(kmer)
                minimizer_ith += 1

    def __read_from_partition_and_write_kmer(self, file_fullpath, lock):
        partition_reader = SuperKmerReader(file_fullpath, self.__k, file_fullpath[:-3])
        i = 0
        partition_size = partition_reader.get_file_lenght()
        gerbil_utils = DefaultGerbilUtils(self.__k, self.__m)
        hash_table = gerbil_utils.get_empty_hash_map()
        while i < partition_size:
            kmer = partition_reader.read_next_kmer()
            if kmer in hash_table:
                hash_table[kmer] = hash_table[kmer] + 1
            else:
                hash_table[kmer] = 1
        lock.acquire()
        dct = {k: [v] for k, v in hash_table.items()}
        pd.DataFrame.from_dict(data=dct, orient='index').to_csv(self.__output_path, mode='a', index=True)
        lock.release()

    def start_second_phase_process(self):
        process_list = list()
        dh = DefaultDirectoryHandler(self.__partition_path)
        file_list = dh.get_all_files_names()
        for file in file_list:
            p = Process(target=self.__process_read_and_write_minimizer, args=(file,))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()
