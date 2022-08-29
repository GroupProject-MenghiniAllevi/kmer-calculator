import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo


class InfoTest(unittest.TestCase):

    def test_create_partitions(self):
        # file1 = 1504
        # file19 = 1498
        # file20 = 1495
        path = self.__get_path()
        # dsk_algorithm = DefaultDskAlgorithm(10,1024,1024,path)
        dsk_info = DefaultDSKInfo(path, 10)
        self.assertEqual(4470, dsk_info.getFullKmerNumber(),
                         "il numero che viene fuori da getFullKmerNumber è: " + str(dsk_info.getFullKmerNumber()))

    def test_iteration_number(self):
        path = self.__get_path()
        dsk_info = DefaultDSKInfo(path, 10)
        dsk_info.getFullKmerNumber()
        self.assertEqual(140, dsk_info.iteration_number(1024))
    def test_partition_number(self):
        path = self.__get_path()
        dsk_info = DefaultDSKInfo(path,10)
        dsk_info.getFullKmerNumber()
        dsk_info.iteration_number(1024)
        #previsto 3
        self.assertEqual(3,dsk_info.get_partition_number(1024))

    def __get_partitions_path(self):
        path = self.__get_path()
        path = os.path.join(path, "partitions")
        return path

    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        return path


if __name__ == '__main__':
    unittest.main()
