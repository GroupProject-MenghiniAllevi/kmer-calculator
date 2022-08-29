import os
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
        return self.__lenght_file(full_path)

    def get_all_files_names(self):
        return [f for f in os.listdir(self.__path) if os.path.isfile(os.path.join(self.__path, f))]

    def get_partition_file_size(self, k, filename):
        fullpath = os.path.join(self.__path,filename)
        counter = 0
        with open(fullpath,"rb") as f:
            while True:
                b = f.read(k)
                if not b:
                    f.close()
                    break
                else:
                    counter+=1


    def __lenght_file(self, full_path):
        char_counter = 0
        with open(full_path, "rb") as file:
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            while True:
                c = file.read(1)
                if c == b'\n':
                    break
                elif c != b'\r':
                    char_counter = char_counter + 1
            file.close()
        return char_counter


