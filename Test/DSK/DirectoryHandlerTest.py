import os
import unittest
from Main.kmer.Utils.Reader.DefaultDirectoryHandler import DefaultDirectoryHandler
from pathlib import Path


class MyTestCase(unittest.TestCase):



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
