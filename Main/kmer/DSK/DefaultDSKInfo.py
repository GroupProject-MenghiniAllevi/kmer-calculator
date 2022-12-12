import os.path

from Main.kmer.DSK.DSKInfo import DSKInfo
import numpy as np
import math

from Main.kmer.Utils.Reader.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.Reader.FastaReader import FastaRnaReader


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
        kmer_reader = FastaRnaReader()
        kmer_reader.set_kmer_lenght(self.__k)
        filelist = dh.get_all_files_names()
        total_size = 0
        for name in filelist:
            kmer_reader.set_path(os.path.join(self.__path, name))
            size = kmer_reader.get_file_lenght()
            kmer_reader.close_file()
            total_size = total_size + size
        self.__kmerSize = total_size
        return self.__kmerSize

    """
     Questo metodo calcola il numerous totale dei k-mer di tutte le sequenze dwi file
     
    """

    def getSingleKmerNumber(self, filepath, molecule):
        kmer_reader = FastaRnaReader()
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(filepath)
        sequence_size = kmer_reader.get_file_lenght()
        if sequence_size == -1:
            # raise ValueError("errore nel calcolo della dimensione della sequenza nel file: ", filepath)
            pass
        kmer_reader.close_file()
        self.__kmerSize = sequence_size
        print("Il k-mer presenti nel file " + filepath + " sono " + str(sequence_size) + "...")
        return sequence_size

    def iteration_number(self, file_disk_space):
        # self.__check_invalid_kmer_size()
        square = self.__get_square_of_ceil_log_2_k()
        try:
            self.__itaretionNumber = math.ceil(self.__kmerSize * square / file_disk_space)
            return self.__itaretionNumber
        except:
            return 0

    def get_partition_number(self, memory_usage):
        self.__check_invalid_iteration_number()
        numerator = self.__kmerSize * (self.__get_square_of_ceil_log_2_k() + 32)
        denominator = 0.7 * self.__itaretionNumber * memory_usage
        self.__partitionNumber = math.ceil(numerator / denominator)
        return self.__partitionNumber

    def __get_log_2_k(self):
        double_k_size = 2 * self.__k
        log = math.log(double_k_size, 2)
        return log

    def __get_square_of_ceil_log_2_k(self):
        ceil_log = math.ceil(self.__get_log_2_k())
        return np.power(2, ceil_log)

    def __check_invalid_kmer_size(self):
        if self.__kmerSize == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di kmer...")

    def __check_invalid_iteration_number(self):
        self.__check_invalid_kmer_size()
        if self.__itaretionNumber == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di iterazioni...")
