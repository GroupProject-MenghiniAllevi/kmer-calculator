from os import listdir
from os.path import isfile, join

from it.unicam.cs.groupproject.kmer.DSK.DirectoryHandler import DirectoryHandler


class DefaultDirectoryHandler(DirectoryHandler):
    __path = ""

    def __init__(self, path):
        self.__path = path

    def set_directory_path(self, path):
        self.__path = path

    def get_directory_path(self):
        return self.__path

    def get_file_size(self, filename):
        full_path = self.__path + "/" + filename
        line_counter = 0
        char_counter = 0
        return self.__lenght_file(full_path, line_counter, char_counter)

    def read_next_kmer_from_file(self, filename):
        pass

    def get_all_files_names(self):
        return [f for f in listdir(self.__path) if isfile(join(self.__path, f))]

    def __lenght_file(self, full_path, line_counter, char_counter):
        with open(full_path, "rb") as file:
            while True:
                c = file.read(1)
                print("char: ", c, " line_counter: ", line_counter, " char_counter: ", char_counter)
                if c == b'\n':
                    line_counter = line_counter + 1
                if line_counter == 4 and c != b'\n':
                    char_counter = char_counter + 1
                elif line_counter > 4:
                    break
        return char_counter
