from Main.kmer.Utils.Reader.KmerReader import KmerReader


class SuperKmerReader(KmerReader):
    __file_path = ""
    __m = 0
    __k = 0
    __minimizer = b""
    __super_kmer_size = 0
    __ith = 0
    __size_counter = 0

    def __init__(self, file_path, k, minimizer):
        self.__file = None
        self.__file_path = file_path
        self.__k = k
        self.__m = len(minimizer)
        self.__super_kmer_size = k - self.__m
        self.__minimizer = minimizer
        self.__ith = self.__super_kmer_size
        self.__file = open(file_path, "rb")

    def read_next_kmer(self):
        super_kmer = self.__file.read(self.__super_kmer_size)
        super_kmer = super_kmer.decode("utf-8")
        if self.__ith == self.__super_kmer_size:
            kmer = super_kmer + self.__minimizer
        elif self.__ith == 0:
            kmer = self.__minimizer + super_kmer
        else:
            kmer = super_kmer[:self.__ith] + self.__minimizer + super_kmer[self.__ith:]
        self.__ith -= 1
        if self.__ith < 0:
            self.__ith = self.__super_kmer_size
        self.__size_counter += 1
        return kmer

    def set_kmer_lenght(self, k):
        self.__k = k

    def set_path(self, path):
        if not self.__file.closed:
            self.__file.close()
        self.__ith = self.__super_kmer_size
        self.__size_counter = 0
        self.__file_path = path
        self.__file = open(path, "rb")

    def has_next(self, kmer_size):
        if self.__size_counter <= kmer_size:
            return True
        else:
            self.__file.close()
            return False

    def get_file_lenght(self):
        counter = 0
        print(self.__file_path)
        with open(self.__file_path, "rb") as f:
            while True:
                r = f.read(self.__super_kmer_size)
                if not r:
                    break
                else:
                    counter += 1
            f.seek(0,0)
            f.close()
        return counter

    def set_minimizer(self, minimizer):
        self.__minimizer = minimizer
        self.__m = len(minimizer)