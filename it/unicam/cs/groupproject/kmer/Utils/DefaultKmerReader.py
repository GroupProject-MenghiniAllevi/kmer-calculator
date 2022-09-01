from it.unicam.cs.groupproject.kmer.Utils.KmerReader import KmerReader


class DefaultKmerReader(KmerReader):
    __k = 0

    __path = ""

    __file = None
    __index = 0

    def __init__(self):
        pass

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
        if not self.__index < kmer_size:
            self.__file.close()
        else:
            return True

    def set_kmer_lenght(self, k):
        if k > 0:
            self.__k = k
        else:
            ValueError("k deve essere maggiore di 0... ")

    def set_path(self, path):
        self.__path = path
        self.__prepare_file()

    def __prepare_file(self):
        self.__file = open(self.__path, "rb")
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()

    def get_file_lenght(self):
        char_counter = 0
        self.__prepare_file()
        while True:
            c = self.__file.read(1)
            if c == b'\n':
                break
            elif c != b'\r':
                char_counter = char_counter + 1
        self.__file.close()
        self.__prepare_file()
        return char_counter
