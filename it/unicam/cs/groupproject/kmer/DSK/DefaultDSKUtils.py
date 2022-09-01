from it.unicam.cs.groupproject.kmer.DSK.DSKUtils import DSKUtils
import hashlib


class DefaultDSKUtils(DSKUtils):
    __iterations_number = int

    __partitions_number = int

    __partionion_index = int

    __iteration_index: int

    __kmer = ""

    __prova = False

    __lock = None

    def __init__(self, index, kmer):
        self.__iterations_index = index
        self.__kmer = kmer

    def equals_to_ith_iteration(self):
        return (self.get_hash() % self.__iterations_number) == self.__iterations_index

    def set_partition_index(self):
        self.__partionion_index = int((self.get_hash() / self.__iterations_number) % self.__partitions_number)

    def set_iteration_number(self, iteration_number):
        self.__iterations_number = iteration_number

    def set_partition_number(self, partition_number):
        self.__partitions_number = partition_number

    def get_hash(self):
        bb = str.encode(self.__kmer)
        hash = int.from_bytes(hashlib.md5(bb).digest()[:8], 'little')
        return hash

    def write_to_partitions(self, path, kmer, lock):
        file = open(path, "a+b")
        byte_kmer = str.encode(kmer)
        file.write(byte_kmer)
        file.close()

    def get_partition_index(self):
        return str(self.__partionion_index)
