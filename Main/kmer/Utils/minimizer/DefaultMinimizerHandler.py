import os

from Main.kmer.Utils.minimizer.DefaultMinimizer import DefaultMinimizer
from Main.kmer.Utils.Writer.DefaultSKmerWriter import DefaultSKmerWriter
from Main.kmer.Utils.minimizer.MinimizerHandler import MinimizerHandler
from Main.kmer.Utils.Reader.DefaultKmerReader import DefaultKmerReader


class DefaultMinimizerHandler(MinimizerHandler):
    __kmer_reader = DefaultKmerReader()
    __k = 0
    __m = 0

    def __init__(self, k, m):
        self.__minimizer = ""
        self.__kmer_reader.set_kmer_lenght(k)
        self.__k = k
        self.__m = m

    def get_minimizers_from_kmer(self, kmer):
        self.__minimizer = kmer[-self.__m:]
        return self.__minimizer

    def find_super_kmer_and_write(self, kmer_list: list, minimizer: str, partition_path: str):
        minimizer_obj = DefaultMinimizer(self.__m)
        minimizer_obj.set_minimizer(minimizer)
        for index in range(len(kmer_list)):
            minimizer_obj.add_kmer_without_minimizer(kmer_list[index])
            index += 1
        super_kmer = minimizer_obj.get_super_kmer()
        writer = DefaultSKmerWriter(self.__m, self.__k)
        writer.set_partition_path(partition_path)
        file_path = os.path.join(partition_path, minimizer + ".bin")
        writer.write_super_kmer(minimizer, super_kmer, file_path)

