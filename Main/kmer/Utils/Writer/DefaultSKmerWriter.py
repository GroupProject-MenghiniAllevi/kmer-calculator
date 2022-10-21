import os

from Main.kmer.Utils.Writer.SKmerWriter import SKmerWriter


class DefaultSKmerWriter(SKmerWriter):
    __m = 0
    __k = 0
    __directory_path = ""

    def __init__(self, m, k):
        self.__m = m
        self.__k = k

    def set_partition_path(self, path):
        self.__directory_path = path

    def write_super_kmer(self, minimizer, super_kmer, file_path: str):
        if not os.path.exists(str(file_path)):
            file = open(file_path, "x")
            file.close()
        with open(file_path, "a+b") as file:
            for ele in super_kmer:
                file.write(ele)
            file.flush()
            file.close()
