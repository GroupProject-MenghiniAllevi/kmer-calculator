from it.unicam.cs.groupproject.kmer.DSK.KmerReader import KmerReader


class DefaultKmerReader(KmerReader):
    __k = 0

    __path = ""

    __file = None

    def __init__(self):
        pass

    def read_next_kmer(self):
        if self.__k == 0:
            ValueError("non è stato impostato un valore k!!")
        if self.__file is not None:
            r = self.__file.read(self.__k)
            if b'\n' in r:
                self.__file.close()
                return r.split(b'\n')[0].decode()
            else:
                return r.decode()




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
