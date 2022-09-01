from it.unicam.cs.groupproject.kmer.Utils.KmerReader import KmerReader


class SuperKmerReader(KmerReader):
    __file_path = ""
    __m = 0
    __k = 0
    __minimizer = b""
    __super_kmer_size = 0
    __ith = 0

    def __init__(self, file_path, k, minimizer):
        self.__file = None
        self.__file_path = file_path
        self.__k = k
        self.__m = len(minimizer)
        self.__super_kmer_size = k - self.__m
        self.__minimizer = minimizer
        self.__ith = k - 1

    def read_next_kmer(self):
        super_kmer = self.__file.read(self.__super_kmer_size)
        kmer = super_kmer[:self.__ith] + self.__minimizer + super_kmer[self.__ith:]
        self.__ith -= 1
        if self.__ith == -1:
            self.__ith = self.__k - 1
        return kmer

    def set_kmer_lenght(self, k):
        self.__k = k

    def set_path(self, path):
        self.__file_path = path
        self.__file = open(path, "rb")

    def has_next(self, kmer_size):
        super().has_next(kmer_size)

    def get_file_lenght(self):
        counter = 0
        with open(self.__file_path, "rb") as f:
            while True:
                r = f.read(self.__super_kmer_size)
                if not r:
                    break
                else:
                    counter += 1
            f.close()
        return counter
