import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo


class InfoTest(unittest.TestCase):

    def test_check_kmer_number(self):
        # file1 = 1504
        # file19 = 1498
        # file20 = 1495
        path = self.__get_path()
        dsk_info = DefaultDSKInfo(path, 10)
        self.assertEqual(4470, dsk_info.getFullKmerNumber(),
                         "il numero che viene fuori da getFullKmerNumber è: " + str(dsk_info.getFullKmerNumber()))

    def test_single_file_kmer_lenght(self):
        path = self.__get_path_file()[0]
        dsk_info = DefaultDSKInfo(path, 10)
        self.assertEqual(1495, dsk_info.getSingleKmerNumber(path))
        path = self.__get_path_file()[1]
        dsk_info = DefaultDSKInfo(path, 10)
        self.assertEqual(1489,dsk_info.getSingleKmerNumber(path))
        path = self.__get_path_file()[2]
        dsk_info = DefaultDSKInfo(path, 10)
        self.assertEqual(1486, dsk_info.getSingleKmerNumber(path))

    def test_iteration_number(self):
        path = self.__get_path()
        dsk_info = DefaultDSKInfo(path, 10)
        dsk_info.getFullKmerNumber()
        self.assertEqual(140, dsk_info.iteration_number(1024))

    def test_partition_number(self):
        path = self.__get_path()
        dsk_info = DefaultDSKInfo(path, 10)
        dsk_info.getFullKmerNumber()
        dsk_info.iteration_number(1024)
        # previsto 3
        self.assertEqual(3, dsk_info.get_partition_number(1024))

    def __get_partitions_path(self):
        path = self.__get_path()
        path = os.path.join(path, "partitions")
        return path

    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        return path

    def __get_path_file(self):
        path = self.__get_path()
        path1 = os.path.join(path, "CRW_16S_A_C_1.db")
        path2 = os.path.join(path, "CRW_16S_A_C_19.db")
        path3 = os.path.join(path, "CRW_16S_A_C_20.db")
        return path1,path2,path3


if __name__ == '__main__':
    unittest.main()
