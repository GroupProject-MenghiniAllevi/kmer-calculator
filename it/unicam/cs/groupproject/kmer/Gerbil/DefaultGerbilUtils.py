from multiprocessing import Lock

from it.unicam.cs.groupproject.kmer.Gerbil.DefaultMinimizer import DefaultMinimizer
from it.unicam.cs.groupproject.kmer.Gerbil.DefaultSKmerWriter import DefaultSKmerWriter
from it.unicam.cs.groupproject.kmer.Gerbil.GerbilUtils import GerbilUtils
from it.unicam.cs.groupproject.kmer.Utils.DefaultKmerReader import DefaultKmerReader


class DefaultGerbilUtils(GerbilUtils):


    __kmer_reader = None
    __k = 0
    __m = 0
    __partition_path = ""
    __input_file_length = 0

    def __init__(self, k, m):
        self.__kmer_reader.set_kmer_lenght(k)
        self.__k = k
        self.__m = m

    def get_next_kmer(self):
        if self.__kmer_reader.has_next(self.__k):
            return self.__kmer_reader.read_next_kmer()

    def has_next_kmer(self):
        return self.__kmer_reader.has_next(self.__k)

    def get_minimizers_from_kmer(self, kmer):
        self.__minimizer = kmer[-self.__m:]
        return self.__minimizer

    def find_super_kmer_and_write(self, kmer_list: list, lock: Lock, minimizer:str):
        minimizer = DefaultMinimizer(self.__m)
        minimizer.set_minimizers(self.__minimizer)
        for ele in kmer_list:
            minimizer.add_kmer_without_minimizer(ele)
        writer = DefaultSKmerWriter(self.__m, self.__k)
        writer.set_partition_path(self.__partition_path)
        writer.write_super_kmer(self.__minimizer, minimizer.get_super_kmer(), lock)

    def get_empty_hash_map(self):
        return dict()