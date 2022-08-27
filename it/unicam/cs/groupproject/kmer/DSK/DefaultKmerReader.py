import hashlib

from it.unicam.cs.groupproject.kmer.DSK.KmerReader import KmerReader


class DefaultKmerReader(KmerReader):
    __k = 0

    __path = ""

    __file = None
    __index = 0
    __file_length = -1

    def __init__(self, file_lenght):
        self.__file_length = file_lenght

    def read_next_kmer(self):
        if self.__k == 0:
            ValueError("non è stato impostato un valore k!!")
        if self.__file.closed:
            return '-1'
        if self.__file is not None and self.__file.closed == False:
            r = self.__file.read(self.__k)
            if b'\n' in r:
                self.__file.close()
                return r.split(b'\n')[0].decode()
            else:
                self.__file.seek(-(self.__k - 1), 1)
                self.__index += 1
                return r.decode()

    def has_next(self, kmer_size):
        return self.__index < kmer_size

    def set_kmer_lenght(self, k):
        if k > 0:
            self.__k = k
        else:
            ValueError("k deve essere maggiore di 0... ")

    def set_path(self, path):
        self.__path = path
        self.__file = open(path, "rb")
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()
