import os
import pathlib
import unittest
from it.unicam.cs.groupproject.kmer.DSK.DefaultDirectoryHandler import DefaultDirectoryHandler
from pathlib import Path
import logging as lg
class MyTestCase(unittest.TestCase):


    def test_file_lenght(self):
        dh = self.__get_directory_handler()
        file_lenght = dh.get_file_size("CRW_16S_A_C_1.db")
        self.assertEqual(1504, file_lenght, "la lunghezza del file non è la stessa di quella passata...")

    def test_file_list(self):
        dh = self.__get_directory_handler()
        list = ["CRW_16S_A_C_1.db", "CRW_16S_A_C_19.db", "CRW_16S_A_C_20.db"]
        self.assertEquals(list, dh.get_all_files_names(),
                          " liste differenti... la lista ottenuta dal directory_handler è la seguente: " + str(dh.get_all_files_names()))


    def __get_directory_handler(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        dh = DefaultDirectoryHandler(path=path)
        return dh


if __name__ == '__main__':
    unittest.main()
