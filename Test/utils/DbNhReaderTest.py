import os
import unittest
from pathlib import Path

from Main.kmer.Utils.Reader.FastaReader import FastaRnaReader


class MyTestCase(unittest.TestCase):

    def test_kmer_length(self):
        reader = self.__get_reader(self.__get_path_file1())
        self.assertEqual(15, reader.get_file_lenght())
        reader.close_file()

    def test_kmer_read(self):
        reader = self.__get_reader(self.__get_path_file1())
        size = reader.get_file_lenght()
        kmer_list = list()
        while reader.has_next(size):
            kmer_list.append(reader.read_next_kmer())
        s = self.__get_kmer_list(3, s="GGUUGAUCCUGCCGGGC")
        self.assertEqual(s, kmer_list)

    def test_different_row_sequence(self):
        p = self.__get_diff_row_seq_path()
        self.__write_diff_row_sequence(p)
        reader = self.__get_reader(p)
        size = reader.get_file_lenght()
        self.assertEqual(7, size)
        kmer_list = list()
        while reader.has_next(size):
            kmer_list.append(reader.read_next_kmer())
        s = self.__get_kmer_list(3, s="AAAAAAY.-")
        self.assertEqual(s, kmer_list)

    def __get_diff_row_seq_path(self):
        main = self.__get_main_path()
        p = os.path.join(main, "reader")
        return os.path.join(p, "diff_row_seq.db")

    def __write_diff_row_sequence(self, path):
        s = "fp\nfpa\npfa\nAAAAAAY.-\n"
        with open(path, "wb+") as file:
            file.write(s.encode('utf-8'))
            file.close()

    def __get_reader(self, path):
        reader = FastaRnaReader()
        reader.set_path(path)
        reader.set_kmer_lenght(3)
        return reader

    def __get_kmer_list(self, k, s):
        kmer_size = len(s) - k + 1
        i = 0
        lst = list()
        while i < kmer_size:
            index_kmer_reader = 0
            readed_value = ""
            while index_kmer_reader < k:
                readed_value += s[i]
                i += 1
                index_kmer_reader += 1
            lst.append(readed_value)
            i = i - k + 1
        return lst

    def __get_path_file1(self):
        p = self.__get_main_path()
        p = os.path.join(p, "reader")
        return os.path.join(p, "file1.db")
        pass

    def __get_main_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        return path


if __name__ == '__main__':
    unittest.main()
