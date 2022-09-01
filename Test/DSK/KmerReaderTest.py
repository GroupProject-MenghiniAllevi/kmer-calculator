import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.Utils.DefaultKmerReader import DefaultKmerReader


class MyTestCase(unittest.TestCase):

    def test_kmer_reader(self):
        file_reader = self.__initialize_file_reader()
        r = file_reader.read_next_kmer()
        l = "ACUCCGGUUG"
        self.assertEqual(l, r, " la stringa letta dal metodo è: " + str(r))
        self.__check_last_string_test(file_reader)

    def __initialize_file_reader(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "CRW_16S_A_C_1.db")
        file_reader = DefaultKmerReader()
        file_reader.set_path(path)
        file_reader.set_kmer_lenght(10)
        return file_reader

    def __check_last_string_test(self, file_reader):
        i = 0
        c = ""
        while file_reader.has_next(1495):
            c = file_reader.read_next_kmer()
            i = i + 1
        self.assertEqual("UCACCUCNNN", c, "la stringa letta dal metodo è: " + str(c))


if __name__ == '__main__':
    unittest.main()
