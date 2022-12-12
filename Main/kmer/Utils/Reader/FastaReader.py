from Main.kmer.Utils.Reader.KmerReader import KmerReader

ALPHABET = ("A","a", "C","c", "G","g", "U","u", "R","r", "Y","y", "S","s", "W","w", "K","k", "M","m", "B","b", "D","d", "H","h", "V","v", "N","n", "-", ".")


class FastaRnaReader(KmerReader):
    __path = ""
    __file = None
    __k = 0
    __size = 0
    __actual_index = 0
    __sequence_row = 0

    def __init__(self):
        pass

    def read_next_kmer(self):
        # print("sequence_row:", self.__sequence_row)
        kmer = self.__file.read(self.__k).decode('utf-8').upper()
        r = -(self.__k - 1)
        self.__file.seek(r, 1)
        self.__actual_index += 1
        return kmer

    def __detect_sequence_row(self):
        self.__file.seek(0, 0)
        actual_line = 1
        checked_value = True
        while True:
            c = self.__file.read(1)
            if not c:
                break
            elif not c or c == b"\r" or c == b"\n":
                # print(c, checked_value, actual_line)
                if checked_value:
                    return actual_line
                else:
                    checked_value = True
                    actual_line += 1
            elif checked_value:
                checked_value = self.__check_byte_value(c)
            if not checked_value:
                self.__file.readline()
                actual_line+=1
                checked_value = True
        return actual_line

    def __check_byte_value(self, b1: bytes):
        s1 = b1.decode('utf-8')
        return s1 in ALPHABET

    def set_kmer_lenght(self, k):
        if k > 0:
            self.__k = k
        else:
            ValueError("k deve essere maggiore di 0... ")

    def set_path(self, path):
        self.__path = path
        self.__file = open(path, "rb")
        self.__sequence_row = self.__detect_sequence_row()
        # print("la sequenza del file "+str(path)+" è alla riga "+str(self.__sequence_row))

    def has_next(self, kmer_size):
        if self.__actual_index < kmer_size and not self.__file.closed:
            return True
        else:
            self.__file.close()
            return False

    def __seek_file_to_row(self):
        i = 1
        self.__file.seek(0, 0)
        while i <= self.__sequence_row:
            if i == self.__sequence_row:
                break
            else:
                self.__file.readline()
                i += 1

    def get_file_lenght(self):
        index = 0
        self.__seek_file_to_row()
        while True:
            c = self.__file.read(1)
            if not c or c == b"\r" or c == b"\n":
                break
            else:
                index += 1
        i = index - self.__k + 1
        self.__size = i
        self.__seek_file_to_row()
        return i

    def close_file(self):
        if not self.__file.closed:
            self.__file.close()
