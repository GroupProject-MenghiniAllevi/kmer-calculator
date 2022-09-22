import os
import shutil
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.Gerbil.SuperKmerReader import SuperKmerReader


class MyTestCase(unittest.TestCase):

    def test_single_reader(self):
        self.__write_file()
        r = SuperKmerReader(self.__get_partitions_path("UGU"), 5, "UGU")
        index = 0
        list_kmer = list()
        expected = ("ACUGU", "CUGUG", "UGUGA")
        size = r.get_file_lenght()

        while r.has_next(size-1):
            c = r.read_next_kmer()
            list_kmer.append(c)
            index += 1
        print(list_kmer)
        for el in list_kmer:
            self.assertTrue(el in expected, el + " non è dentro")
        self.__delete_all_partition(self.__get_partitions_path("UGU"))

    def __delete_all_partition(self, partition_path):
        os.remove(partition_path)

    def test_multiple_writing(self):
        self.__write_file_multiple_skmer()
        r = SuperKmerReader(self.__get_partitions_path("UGU"), 5, "UGU")
        index = 0
        list_kmer = list()
        expected = ("ACUGU", "CUGUG", "UGUGA", "AUUGU", "UUGUA", "UGUAG")
        while r.has_next(r.get_file_lenght()-1):
            c = r.read_next_kmer()
            list_kmer.append(c)
            index += 1
        print(list_kmer)
        for el in list_kmer:
            self.assertTrue(el in expected, el + " non è dentro")
        self.__delete_all_partition(self.__get_partitions_path("UGU"))

    def test_different_super_kmer(self):
        partition_path1 = self.__get_partitions_path("GGUCG")
        partition_path2 = self.__get_partitions_path("UCCUG")
        self.__write_multiple_super_kmer(partition_path1,partition_path2)
        r1 = SuperKmerReader(self.__get_partitions_path("GGUCG"),10,"GGUCG")
        r2 = SuperKmerReader(self.__get_partitions_path("UCCUG"),10,"UCCUG")
        kmer_list = list()
        size1 = r1.get_file_lenght()
        print(size1)
        while r1.has_next(size1-1):
            kmer = r1.read_next_kmer()
            kmer_list.append(kmer)
        size2 = r2.get_file_lenght()
        while r2.has_next(size2-1):
            kmer = r2.read_next_kmer()
            kmer_list.append(kmer)
        self.__check_different_super_kmer(kmer_list)
        self.__delete_all_partition(self.__get_partitions_path("GGUCG"))
        self.__delete_all_partition(self.__get_partitions_path("UCCUG"))

    def test_file_length(self):
        self.__write_file_lenght()
        r = SuperKmerReader(self.__get_partitions_path("AGCA"), 9, "AGCA")
        self.assertEqual(6,r.get_file_lenght())
        size = r.get_file_lenght()
        while r.has_next(size-1):
            r.read_next_kmer()
        self.__delete_all_partition(self.__get_partitions_path("AGCA"))

    def __write_multiple_super_kmer(self,GGUCG, UCCUG):
        with open(GGUCG,"wb") as f:
            f.write(b"ACUCCCUCCAUCCAUCCAUCCAUCCAUCCU")
            f.close()
        with open(UCCUG,"wb") as f:
            f.write(b"GUCGAUCGACCGACCGACCGACCGGCCGGC")
            f.close()
    def __write_file(self):
        path = self.__get_partitions_path("UGU")
        with open(path, "wb") as f:
            # minimizer: UGU
            f.write(b"ACCGGA")
            f.close()

        pass

    def __get_partitions_path(self,name):
        name = name + ".bin"
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        path = os.path.join(path, name)
        print("partition_path: ", path)
        return path

    def __write_file_multiple_skmer(self):
        path = self.__get_partitions_path("UGU")
        with open(path, "wb") as f:
            f.write(b"ACCGGAAUUAAG")
            f.close()

    def __write_file_lenght(self):
        path = self.__get_partitions_path("AGCA")
        with open(path,"wb") as f:
            f.write(B"CAGGCAGGCCGGCCCGCCCGCCCGACCGAA")
            f.close()

    def __check_different_super_kmer(self, kmer_list):
        expected = ["ACUCCGGUCG","CUCCGGUCGA","UCCGGUCGAU","CCGGUCGAUC","CGGUCGAUCC","GGUCGAUCCU","GUCGAUCCUG","UCGAUCCUGC","CGAUCCUGCC","GAUCCUGCCG","AUCCUGCCGG","UCCUGCCGGC"]
        self.assertEqual(len(expected),len(kmer_list))
        for el in kmer_list:
            self.assertEqual(10,len(el))
            self.assertTrue(el in expected)
        pass


if __name__ == '__main__':
    unittest.main()
