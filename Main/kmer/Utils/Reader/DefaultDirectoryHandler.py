import os

from Main.kmer.Utils.DirectoryHandler import DirectoryHandler
FASTA_EXTENSION = ".fasta"

class DefaultDirectoryHandler(DirectoryHandler):
    __path = ""

    def __init__(self, path):
        self.__path = path

    def set_directory_path(self, path):
        self.__path = path

    def get_directory_path(self):
        return self.__path

    def get_all_files_names(self):
        return [f for f in os.listdir(self.__path) if os.path.isfile(os.path.join(self.__path, f)) and f.endswith(".db") or f.endswith(FASTA_EXTENSION)]

    def get_partition_file_size(self, k, filename):
        fullpath = os.path.join(self.__path, filename)
        counter = 0
        with open(fullpath, "rb") as f:
            while True:
                b = f.read(k)
                if not b:
                    f.close()
                    break
                else:
                    counter += 1
