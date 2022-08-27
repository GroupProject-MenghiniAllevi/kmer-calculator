import os
import threading
from multiprocessing.pool import Pool
from pathlib import Path
import multiprocessing as mp
import numpy as np
from it.unicam.cs.groupproject.kmer.DSK.DSKAlgorithm import DSKAlgorithm
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKUtils import DefaultDSKUtils
from it.unicam.cs.groupproject.kmer.DSK.DefaultDirectoryHandler import DefaultDirectoryHandler
from it.unicam.cs.groupproject.kmer.DSK.DefaultKmerReader import DefaultKmerReader
from it.unicam.cs.groupproject.kmer.DSK.DirectoryHandler import DirectoryHandler


class DefaultDskAlgorithm(DSKAlgorithm):
    __k = 0

    __diskUsage = 0

    __memoryUsage = 0

    __path = ""

    __iteration_number = 0

    __partition_number = 0

    __dsk_info = None

    __partition_path = ""
    __kmer_size: int

    def __init__(self, k, memory_usage, disk_usage, path):
        self.__kmer_size = 0
        self.__k = k
        self.__memoryUsage = memory_usage
        self.__diskUsage = disk_usage
        self.__path = path
        self.__initialize_values()
        """
        Metodo costruttore della classe

        """

    def set_iteration_number(self):
        self.__iteration_number = self.__dsk_info.iteration_number(self.__diskUsage)

    """
    Qeusto metodo imposta il numero delle iterazioni
    """

    def set_partition_number(self):
        self.__partition_number = self.__dsk_info.get_partition_number(self.__memoryUsage)

    """
    Questo metodo imposta il numero delle partizioni
    """

    def create_partition_files(self, partition_path):
        self.__partition_path = partition_path
        p = 0
        while p < self.__partition_number:
            file_name = "partition-" + str(p) + ".bin"
            print(file_name)
            fullpath = os.path.join(self.__partition_path, file_name)
            if os.path.exists(str(fullpath)):
                file = open(fullpath,"r+")
                file.truncate()
            else:
                file = open(fullpath, "x")

            file.close()
            p = p + 1

    """
    Questo metodo crea i file delle partizioni 
    """

    def process(self, partition_path):
        self.__partition_path = partition_path
        for i in range(self.__iteration_number):
            self.create_partition_files(partition_path)
            self.save_to_partitions(i)
            self.write_to_output()
    def initialize_hash_table(self):
        ht = {int:bytes}
        return ht




    def thread_partitions_write(self, filename, j, k_number):
        kmer_reader = DefaultKmerReader(self.__kmer_size)
        print("kmer_size: ",self.__kmer_size)
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(self.__path + "/" + filename)
        while kmer_reader.has_next(k_number):
            kmer = kmer_reader.read_next_kmer()
            dsk_utils = DefaultDSKUtils(j, kmer)
            dsk_utils.set_partition_number(self.__partition_number)
            dsk_utils.set_iteration_number(self.__iteration_number)
            if dsk_utils.equals_to_ith_iteration():
                dsk_utils.set_partition_index()
                fullpath = self.__partition_path + "/partition-" + dsk_utils.get_partition_index() + ".bin"
                dsk_utils.write_to_partitions(fullpath, kmer)
    def save_to_partitions(self, i):
        list_of_file = self.__list_of_file_lenght()
        j = 0
        pool = Pool(4)
        for file in list_of_file:
            dh = DefaultDirectoryHandler(self.__path)
            size = dh.get_file_size(file)
            pool.apply_async(self.thread_partitions_write, (j, self.__dsk_info.getSingleKmerNumber(size)))
            j = j + 1
        pool.close()


    def write_to_output(self):
        for j in range(self.__partition_number):
            hash_table = self.initialize_hash_table()  #    line 13
            kmer_reader = DefaultKmerReader(self.__kmer_size)
            kmer_reader.set_kmer_lenght(self.__k)
            kmer_reader.set_path(self.__partition_path + "/partition-"+str(j)+".bin")
            dh = DefaultDirectoryHandler(self.__partition_path)
            size = dh.get_file_size(self.__partition_path + "/partition-"+str(j)+".bin")
            k_number = self.__dsk_info.getSingleKmerNumber(size)
            while kmer_reader.has_next(k_number):
                pass

    def __initialize_values(self):
        self.__dsk_info = DefaultDSKInfo(self.__path, self.__k)
        self.__kmer_size = self.__dsk_info.getFullKmerNumber()

    def __list_of_file_lenght(self):
        dh = DefaultDirectoryHandler(self.__path)
        return dh.get_all_files_names()

    def __get_kmer_partition_number_total(self, filename):
        dh = DefaultDirectoryHandler(self.__partition_path)
        return dh.get_partition_file_size(self.__k,filename)