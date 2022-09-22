import multiprocessing
import os

from it.unicam.cs.groupproject.kmer.Gerbil.SKmerWriter import SKmerWriter


class DefaultSKmerWriter(SKmerWriter):
    __m = 0
    __k = 0
    __directory_path = ""

    def __init__(self, m, k):
        self.__m = m
        self.__k = k

    def set_partition_path(self, path):
        self.__directory_path = path

    def write_super_kmer(self, minimizer, super_kmer, lock: multiprocessing.Lock(), file_path:str):
        if not os.path.exists(str(file_path)):
            f = open(file_path, "x")
            f.close()
        with open(file_path, "ab") as f:
            for ele in super_kmer:
                f.write(ele)
            f.close()

