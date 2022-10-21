from Main.kmer.Utils.Reader.KmerReader import KmerReader


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
        if self.__file is not None and self.__file.closed == False:
            r = self.__file.read(self.__k)
            self.__file.seek(-(self.__k - 1), 1)
            self.__index += 1
            #print("value:", r)
            return r.decode()

    def has_next(self, kmer_size):
        if self.__index < kmer_size and not self.__file.closed:
            return True
        else:
            self.__file.close()
            return False

    def set_kmer_lenght(self, k):
        if k > 0:
            self.__k = k
        else:
            ValueError("k deve essere maggiore di 0... ")

    def set_path(self, path):
        self.__path = path
        self.__file = open(path, "rb")
        self.__prepare_file()

    def __prepare_file(self):
        self.__file.seek(0, 0)
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()
        self.__file.readline()

    def get_file_lenght(self):
        char_counter = 0
        self.__prepare_file()
        while True:
            c = self.__file.read(self.__k)
            if not c or b'\n' in c or b'\r' in c:
                break
            else:
                char_counter = char_counter + 1
                self.__file.seek(-self.__k + 1, 1)
        self.__prepare_file()

        return char_counter

    def close_file(self):
        if not self.__file == None and not self.__file.closed:
            self.__file.close()

    def get_file_name(self):
        """
        Questo metodo restituisce il nome della molecola contenuta nel file che si sta analizzando.
        :return: una stringa contenente il nome della molecola del file.
        """
        name = ""
        read = False
        if not self.__file.closed:
            self.__file.seek(0,0)
            while True:
                c = self.__file.read(1)
                if not c or c == b"\r" or c == b"\n":
                    break
                elif c == b" ":
                    read = True
                if read:
                    s = c.decode('utf-8')
                    name+=s
        return name
