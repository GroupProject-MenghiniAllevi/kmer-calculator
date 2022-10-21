import os
import shutil
import unittest
from pathlib import Path

from Main.kmer.Utils.minimizer.DefaultMinimizerHandler import DefaultMinimizerHandler


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_write_minimizers(self):
        g_utils = DefaultMinimizerHandler(3, 2)
        self.assertEqual("CU", g_utils.get_minimizers_from_kmer("ACU"))
        g_utils = DefaultMinimizerHandler(3, 2)
        self.assertEqual("CC", g_utils.get_minimizers_from_kmer("UCC"))
        g_utils = DefaultMinimizerHandler(3, 2)
        self.assertEqual("GG", g_utils.get_minimizers_from_kmer("CGG"))

    def test_write_kmer_to_partition(self):
        g_utils = DefaultMinimizerHandler(3, 2)
        kmer_list = self.__get_kmer_list()
        minimizer = g_utils.get_minimizers_from_kmer("ACU")
        self.write_and_check_file(kmer_list,minimizer,g_utils,"CU.bin","file1.db","AC")
        minimizer = g_utils.get_minimizers_from_kmer("UCC")
        self.write_and_check_file(kmer_list, minimizer, g_utils, "CC.bin", "file1.db","UG")
        minimizer = g_utils.get_minimizers_from_kmer("CGG")
        self.write_and_check_file(kmer_list, minimizer, g_utils, "GG.bin", "file1.db","CU")
        p = self.__get_partitions_path()
        p = os.path.join(p,"file1.db")
        shutil.rmtree(p)

    def write_and_check_file(self,kmer_list,minimizer,g_utils,filename,partname,expected_value):
        p = self.__generate_partitions(partname)
        file_path = os.path.join(p, filename)
        l1 = kmer_list[0:1]
        g_utils.find_super_kmer_and_write(kmer_list, minimizer, p)
        readed_value = self.__read_value_from_file(file_path)
        self.assertEqual(expected_value, readed_value)

    def __read_value_from_file(self,file_path):
        with open(file_path, "rb") as file:
            readed_value = file.read().decode('utf-8')
            file.close()
        return readed_value

    def __get_kmer_list(self):
        l = list()
        l.append("ACU")
        l.append("CUC")
        l.append("UCC")
        l.append("CCG")
        l.append("CGG")
        l.append("GGU")
        return l

    def __generate_partitions(self, subfolder):
        path = self.__get_partitions_path()
        path_p1 = os.path.join(path, subfolder)
        if os.path.exists(path_p1):
            shutil.rmtree(path_p1)
        os.mkdir(path_p1)
        return path_p1

    def __get_partitions_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        return path


if __name__ == '__main__':
    unittest.main()
