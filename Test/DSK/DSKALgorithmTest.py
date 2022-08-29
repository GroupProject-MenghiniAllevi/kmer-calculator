import array
import os
import time
import unittest
from pathlib import Path

import numpy as np

from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKAlgorithm import DefaultDskAlgorithm


class MyTestCase(unittest.TestCase):

    def test_partitions_saves(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        dsk_algorithm.create_partition_files(self.__get_partitions_path())
        p0 = self.__get_partition_file_path()[0]
        self.assertTrue(p0.is_file())
        p1 = self.__get_partition_file_path()[1]
        self.assertTrue(p1.is_file())
        os.remove(p0)
        os.remove(p1)

    def __get_partition_file_path(self):
        return Path(os.path.join(self.__get_partitions_path(), "partition-0.bin")), Path(
            os.path.join(self.__get_partitions_path(), "partition-1.bin"))

    def __get_dsk_algorithm(self):
        dsk_algorithm = DefaultDskAlgorithm(3, 1024, 1024, self.__get_path())
        print(self.__get_path())
        dsk_algorithm.set_iteration_number()
        dsk_algorithm.set_partition_number()
        return dsk_algorithm

    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "test_algorithm")
        return path

    def __get_output_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "output")
        path = os.path.join(path, "out.csv")
        return path

    def test_kmer_strings(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        dsk_algorithm.create_partition_files(self.__get_partitions_path())
        dsk_algorithm.thread_partitions_write("file1.db", 0, 6)
        list_of_kmer_inside_file1 = self.__get_kmer_from_files1()
        self.__check_kmer_inside_partition(0, list_of_kmer_inside_file1)
        os.remove(self.__get_partition_file_path()[0])
        os.remove(self.__get_partition_file_path()[1])

    def test_all_kmer_strings(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        dsk_algorithm.create_partition_files(self.__get_partitions_path())
        dsk_algorithm.thread_partitions_write("file1.db", 0, 6)
        dsk_algorithm.thread_partitions_write("file2.db", 0, 15)
        self.__check_kmer_inside_partition(0, self.__get_kmer_from_files1_and_2())

    def __get_partitions_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        return path

    def __get_kmer_from_files1(self):
        return "ACUCUCUCCCCGCGGGGU"

    def __get_kmer_from_files1_and_2(self):
        return self.__get_kmer_from_files1() + "GGUGUUUUGUGAGAUAUCUCCCCUCUGUGCGCCCCGCGGGGGGGC"

    def __check_kmer_inside_partition(self, i, list_of_kmer_inside_file1):
        path = self.__get_partition_file_path()[i]
        bb = self.__read_from_file(path)
        self.assertEqual(bb, str(list_of_kmer_inside_file1))

    def __read_from_file(self, path):
        bb = ""
        with open(path, "rb") as f:
            while True:
                app = f.read()
                if not app:
                    break
                else:
                    app1 = app.decode('UTF-8')
                    bb = str(app1) + bb
        return bb

    def test_full_algorithm(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        dsk_algorithm.process(self.__get_partitions_path(), self.__get_output_path())
        self.__check_out_file()

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
