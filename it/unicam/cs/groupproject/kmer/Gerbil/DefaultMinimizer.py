import array

from it.unicam.cs.groupproject.kmer.Gerbil.Minimizers import Minimizers


class DefaultMinimizer(Minimizers):
    __m = 0

    __minimizer = bytearray()

    __super_kmer = None

    def __init__(self, m):
        if m <= 0:
            ValueError("la dimensione del minimizer è mnore o uguale a 0...")
        self.__m = m
        self.__super_kmer = list()

    def set_minimizers(self, minimizer):
        self.__minimizer = minimizer

    def add_kmer_without_minimizer(self, kmer):
        if self.__minimizer == "":
            ValueError("minimizer non impostato...")
        minimizer_start_index = kmer.find(self.__minimizer)
        if not minimizer_start_index == -1:
            minimizer_end_index = minimizer_start_index + self.__m
            kmer_without_minimizer = kmer[0:minimizer_start_index:] + kmer[minimizer_end_index::]
            self.__super_kmer.append(kmer_without_minimizer.encode("UTF-8"))



    def get_super_kmer(self):
        return self.__super_kmer
