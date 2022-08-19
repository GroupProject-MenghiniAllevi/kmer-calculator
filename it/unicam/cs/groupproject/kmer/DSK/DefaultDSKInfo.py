import math

from it.unicam.cs.groupproject.kmer.DSK.DSKInfo import DSKInfo
import numpy as np


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

    def getFullKmerNumber(self, sequence_number_list):
        for sequence_size in sequence_number_list:
            self.__kmerSize = self.__kmerSize + self.getSingleKmerNumber(sequence_size)
        return self.__kmerSize

    """
     Questo metodo calcola il numero totale dei k-mer di tutte le sequenze dwi file
     
    """

    def getSingleKmerNumber(self, sequence_size):
        return sequence_size - self.__k + 1

    def iteration_number(self, file_disk_space):
        self.__check_invalid_kmer_size()
        self.__itaretionNumber = self.__kmerSize * np.power(2, math.log(2 * self.__k, 2)) / file_disk_space
        return self.__itaretionNumber

    def get_partition_number(self, memory_usage):
        self.__check_invalid_iteration_number()
        self.__partitionNumber = self.__kmerSize * (np.power(2, math.log(2 * self.__k, 2)) * 2) / (
                    0.7 * self.__itaretionNumber * memory_usage)
        return self.__partitionNumber

    def __check_invalid_kmer_size(self):
        if self.__kmerSize == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di kmer...")

    def __check_invalid_iteration_number(self):
        self.__check_invalid_kmer_size()
        if self.__itaretionNumber == -1:
            raise ValueError("bisogna prima calcolare la quantità totale di iterazioni...")
