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
        full_path = self.__path + filename
        line_counter = 0
        char_counter = 0
        with open(full_path, "rb") as file:
            while True:
                c = file.read(1)
                if line_counter == 4:
                    char_counter += 1
                elif line_counter > 4:
                    break
                elif c == '\n':
                    line_counter += 1
        return char_counter

    def read_next_kmer_from_file(self, filename):
        super().read_next_kmer_from_file(filename)

    def get_all_files_names(self):
        super().get_all_files_names()
