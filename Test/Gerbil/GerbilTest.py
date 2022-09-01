import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.Gerbil.DefaultGerbil import DefaultGerbil


class MyTestCase(unittest.TestCase):


    def test_full_algorithm(self):
        gerbil = DefaultGerbil(self.__get_path(),self.__get_partitions_path(),self.__get_output_path,3,2)
        gerbil.process()
        self.__check_out_file()


    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "test_algorithm")
        return path

    def __get_partitions_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        return path

    def __get_output_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "output")
        path = os.path.join(path, "out.csv")
        return path


    def __check_out_file(self):
        with open(self.__get_output_path(), "r") as f:
            lines = f.readlines()
            j = 0
            values = list()
            index = list()
            for line in lines:
                if j != 0:
                    str_arr = line.split(",")
                    if len(str_arr) == 2:
                        index.append(str_arr[0])
                        values.append(str_arr[1])
                else:
                    j = 1
            arr_expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                            'GGG', 'GGC', 'ACU', 'CUC', 'UCC', 'CCG', 'CGG', 'GGU']
            for i in range(len(arr_expected)):
                self.assertEqual(True, arr_expected[i] in index, "non è stato trovato l'elemento... " + arr_expected[i])
            print(index)


if __name__ == '__main__':
    unittest.main()
