import os
import unittest
from pathlib import Path

from Main.kmer.Utils.Reader.DefaultKmerReader import DefaultKmerReader


class MyTestCase(unittest.TestCase):

    def test_kmer_reader(self):
        file_reader = self.__initialize_file_reader()
        r = file_reader.read_next_kmer()
        l = "ACUCCGGUUG"
        self.assertEqual(l, r, " la stringa letta dal metodo è: " + str(r))
        self.__check_last_string_test()

    def __initialize_file_reader(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "CRW_16S_A_C_1.db")
        file_reader = DefaultKmerReader()
        file_reader.set_path(path)
        file_reader.set_kmer_lenght(10)
        return file_reader

    def __check_last_string_test(self):
        file_reader = self.__initialize_file_reader()
        c = ""
        size = file_reader.get_file_lenght()
        i = 0
        cc = ""
        while file_reader.has_next(size):
            c = file_reader.read_next_kmer()
            '''
            if '\n' in c:
                cc = ""
            else:
                cc = c
            '''
            print("index:while: ",i)
            i +=1
        self.assertEqual("UCACCUCNNN", c, "la stringa letta dal metodo è: " + str(c))

    def test_file_lenght(self):
        file_reader = self.__initialize_file_reader()
        self.assertEqual(1495,file_reader.get_file_lenght())

    def test_molecules_names(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "test_algorithm")
        path = os.path.join(path,"file1.db")
        file_reader = DefaultKmerReader()
        file_reader.set_path(path)
        file_reader.set_kmer_lenght(3)
        d = dict()
        d["file1.db"] = "file1"
        actual = file_reader.get_file_name()
        file_reader.close_file()
        for key in actual:
            self.assertTrue(key in actual)

if __name__ == '__main__':
    unittest.main()
