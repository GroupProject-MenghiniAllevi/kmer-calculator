from it.unicam.cs.groupproject.kmer.Utils.KmerReader import KmerReader


class PartitionKmerReader(KmerReader):
    __k = 0

    __file_path = ""

    __file = None
    __index = 0
    __file_length = -1

    def __init__(self, file_path, k):
        self.__k = k
        self.__file_path = file_path
        self.__file = open(file_path, "rb")

    def read_next_kmer(self):
        if self.__k == 0:
            ValueError("non è stato impostato la dimensione del kmer")
        if self.__file is None:
            ValueError("non è stato impostato il path del file")
        self.__index += 1
        return self.__file.read(self.__k)

    def set_kmer_lenght(self, k):
        if k > 0:
            self.__k = k
        else:
            ValueError("k deve essere maggiore di 0... ")

    def set_path(self, path):
        self.__file_path = path
        self.__file = open(self.__file_path, "rb")

    def has_next(self, kmer_size):
        if not (self.__index < self.__file_length):
            self.__file.close()
        else:
            return True

    def get_file_lenght(self):
        counter = 0
        with open(self.__file_path, "rb") as f:
            while True:
                c = f.read(self.__k)
                if  not c:
                   break
                else:
                    counter+=1
        self.__file_length = counter
        return counter
