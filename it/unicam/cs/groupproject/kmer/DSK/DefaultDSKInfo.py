import math

from it.unicam.cs.groupproject.kmer.DSK.DSKInfo import DSKInfo
import numpy as np
import math

from it.unicam.cs.groupproject.kmer.DSK.DefaultDirectoryHandler import DefaultDirectoryHandler


class DefaultDSKInfo(DSKInfo):
    __path = ""
    __kmerSize = -1
    __itaretionNumber = -1
    __partitionNumber = -1
    __k = -1

    def __init__(self, path, k):
        self.__path = path
        self.__k = k
        """
        costruttore della classe
        
        """

    def getFullKmerNumber(self):
        dh = DefaultDirectoryHandler(self.__path)
        filelist = dh.get_all_files_names()
        total_size = 0
        for name in filelist:
            size = dh.get_file_size(name)
            total_size = total_size + self.getSingleKmerNumber(size)
        self.__kmerSize = total_size
        return self.__kmerSize

    """
     Questo metodo calcola il numero totale dei k-mer di tutte le sequenze dwi file
     
    """

    def getSingleKmerNumber(self, sequence_size):
        return sequence_size - self.__k + 1

    def iteration_number(self, file_disk_space):
        self.__check_invalid_kmer_size()
        square = self.__get_square_of_ceil_log_2_k()
        print("square: ", square)
        self.__itaretionNumber = math.ceil(self.__kmerSize * square / file_disk_space)
        return self.__itaretionNumber

    def get_partition_number(self, memory_usage):
        self.__check_invalid_iteration_number()
        self.__partitionNumber = (self.__kmerSize * (np.power(2, math.ceil(self.__get_log_2_k())) + 32)) / (
                0.7 * self.__itaretionNumber * memory_usage)
        return self.__partitionNumber

    def __get_log_2_k(self):
        log = math.log(2 * self.__kmerSize, 2)

        print("log: ", log, " kmersize: ", self.__kmerSize)
        return log

    def __get_square_of_ceil_log_2_k(self):
        ceil_log = math.ceil(self.__get_log_2_k())
        print("ceil: ", ceil_log)
        return np.power(2, ceil_log)

    def __check_invalid_kmer_size(self):
        if self.__kmerSize == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di kmer...")

    def __check_invalid_iteration_number(self):
        self.__check_invalid_kmer_size()
        if self.__itaretionNumber == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di iterazioni...")
