import os
import shutil
import unittest
from pathlib import Path

from Main.kmer.Utils.Reader.SuperKmerReader import SuperKmerReader


class MyTestCase(unittest.TestCase):

    def test_single_reader(self):
        self.__write_file()
        r = SuperKmerReader(self.__get_partitions_path("UGU", "pippo"), 5, "UGU")
        index = 0
        list_kmer = list()
        expected = ("ACUGU", "CUGUG", "UGUGA")
        size = r.get_file_lenght()

        while r.has_next(size - 1):
            c = r.read_next_kmer()
            list_kmer.append(c)
            index += 1
        print(list_kmer)
        for el in list_kmer:
            self.assertTrue(el in expected, el + " non è dentro")
        self.__delete_all_partition("pippo")

    def test_single_reader_not_full(self):
        self.__write_not_full_skmer()
        r = SuperKmerReader(self.__get_partitions_path("CCC","pippo"),6,"CCC")
        expected = ("GUACCC","GUCCCA","GCCCAN","CCCANU","ANNCCC","ANCCCU")
        size = r.get_file_lenght()
        kmer_list = list()
        while r.has_next(size-1):
            kmer = r.read_next_kmer()
            kmer_list.append(kmer)
            self.assertTrue(kmer in expected,"il kmer "+kmer+" non è in "+expected.__str__())
        print(kmer_list)
        self.__delete_all_partition("pippo")
    def __delete_all_partition(self, filename):
        path = self.__get_partition_file_path(filename)
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_multiple_writing(self):
        self.__write_file_multiple_skmer()
        r = SuperKmerReader(self.__get_partitions_path("UGU", "pippo"), 5, "UGU")
        index = 0
        list_kmer = list()
        expected = ("ACUGU", "CUGUG", "UGUGA", "AUUGU", "UUGUA", "UGUAG")
        while r.has_next(r.get_file_lenght() - 1):
            c = r.read_next_kmer()
            list_kmer.append(c)
            index += 1
        print(list_kmer)
        for el in list_kmer:
            self.assertTrue(el in expected, el + " non è dentro")
        self.__delete_all_partition("pippo")

    def test_different_super_kmer(self):
        partition_path1 = self.__get_partitions_path("GGUCG", "pippo")
        partition_path2 = self.__get_partitions_path("UCCUG", "pippo")
        part_path = self.__get_partition_file_path("pippo")
        self.__write_multiple_super_kmer(partition_path1, partition_path2, part_path)
        r1 = SuperKmerReader(self.__get_partitions_path("GGUCG", "pippo"), 10, "GGUCG")
        r2 = SuperKmerReader(self.__get_partitions_path("UCCUG", "pippo"), 10, "UCCUG")
        kmer_list = list()
        size1 = r1.get_file_lenght()
        print(size1)
        while r1.has_next(size1 - 1):
            kmer = r1.read_next_kmer()
            kmer_list.append(kmer)
        size2 = r2.get_file_lenght()
        while r2.has_next(size2 - 1):
            kmer = r2.read_next_kmer()
            kmer_list.append(kmer)
        self.__check_different_super_kmer(kmer_list)
        self.__delete_all_partition("pippo")

    def test_file_length(self):
        self.__write_file_lenght(self.__get_partition_file_path("pippo"))
        r = SuperKmerReader(self.__get_partitions_path("AGCA", "pippo"), 9, "AGCA")
        self.assertEqual(6, r.get_file_lenght())
        size = r.get_file_lenght()
        while r.has_next(size - 1):
            r.read_next_kmer()
        self.__delete_all_partition("pippo")

    def test_multiple_part_path(self):
        minimizers = self.__get_minimizers_multiple_path()
        l = {'pippo': "GCNCNANAUAUC", 'paperino': "AUNUNGNGUGUN", 'pluto': "CCGCGAGAUAUU"}
        self.__write_multiple_path(l, minimizers)
        part_path1 = self.__get_partition_file_path("pippo")
        part_path2 = self.__get_partition_file_path("paperino")
        part_path3 = self.__get_partition_file_path("pluto")
        f_path1 = os.path.join(part_path1, minimizers[0])
        f_path2 = os.path.join(part_path2, minimizers[1])
        f_path3 = os.path.join(part_path3, minimizers[2])
        l1= list()
        l2 = list()
        l3 = list()
        reader = SuperKmerReader(file_path=f_path1, k=6, minimizer=minimizers[0])
        size1 = reader.get_file_lenght()
        while reader.has_next(size1 - 1):
            kmer = reader.read_next_kmer()
            l1.append(kmer)
        reader.set_path(f_path2)
        reader.set_minimizer("NGG")
        size2 = reader.get_file_lenght()
        while reader.has_next(size2 - 1):
            kmer = reader.read_next_kmer()
            l2.append(kmer)
        reader.set_path(f_path3)
        reader.set_minimizer("NNN")
        size3 = reader.get_file_lenght()
        while reader.has_next(size3 - 1):
            kmer = reader.read_next_kmer()
            l3.append(kmer)
        ex_l1 = ['GCNCNN', 'CNCNNA', 'NCNNAU', 'CNNAUC']
        ex_l2 = ['AUNNGG', 'UNNGGG', 'NNGGGU', 'NGGGUN']
        ex_l3 = ['CCGNNN', 'CGNNNA', 'GNNNAU', 'NNNAUU']
        self.assertEqual(ex_l1, l1)
        self.assertEqual(ex_l2, l2)
        self.assertEqual(ex_l3, l3)
        self.__delete_all_partition("pippo")
        self.__delete_all_partition("pluto")
        self.__delete_all_partition("paperino")

    def __write_multiple_super_kmer(self, GGUCG, UCCUG, partition_path):
        if not os.path.exists(partition_path):
            os.mkdir(partition_path)
        with open(GGUCG, "wb") as f:
            f.write(b"ACUCCCUCCAUCCAUCCAUCCAUCCAUCCU")
            f.close()
        with open(UCCUG, "wb") as f:
            f.write(b"GUCGAUCGACCGACCGACCGACCGGCCGGC")
            f.close()

    def __write_file(self):
        path = self.__get_partitions_path("UGU", "pippo")
        part_path = self.__get_partition_file_path("pippo")
        if not os.path.exists(part_path):
            os.mkdir(part_path)
        with open(path, "wb") as f:
            # minimizer: UGU
            f.write(b"ACCGGA")
            f.close()

        pass

    def __get_partitions_path(self, name, molecule_name):
        name = name + ".bin"
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        path = os.path.join(path, molecule_name)
        path = os.path.join(path, name)
        print("partition_path: ", path)
        return path

    def __get_partition_file_path(self, part_path):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        path = os.path.join(path, part_path)
        return path

    def __write_file_multiple_skmer(self):
        path = self.__get_partition_file_path("pippo")
        if not os.path.exists(path):
            os.mkdir(path)
        path = self.__get_partitions_path("UGU", "pippo")
        with open(path, "wb") as f:
            f.write(b"ACCGGAAUUAAG")
            f.close()

    def __write_file_lenght(self, part_path):
        path = self.__get_partitions_path("AGCA", "pippo")
        if not os.path.exists(part_path):
            os.mkdir(part_path)
        with open(path, "wb") as f:
            f.write(B"CAGGCAGGCCGGCCCGCCCGCCCGACCGAA")
            f.close()

    def __check_different_super_kmer(self, kmer_list):
        expected = ["ACUCCGGUCG", "CUCCGGUCGA", "UCCGGUCGAU", "CCGGUCGAUC", "CGGUCGAUCC", "GGUCGAUCCU", "GUCGAUCCUG",
                    "UCGAUCCUGC", "CGAUCCUGCC", "GAUCCUGCCG", "AUCCUGCCGG", "UCCUGCCGGC"]
        self.assertEqual(len(expected), len(kmer_list))
        for el in kmer_list:
            self.assertEqual(10, len(el))
            self.assertTrue(el in expected)
        pass

    def __write_multiple_path(self, paths, minimizers):
        index_m = 0
        for path in paths:
            p = self.__get_partition_file_path(path)
            if not os.path.exists(p):
                os.mkdir(p)
            s = paths[path]
            p = os.path.join(p, minimizers[index_m])
            index_m += 1
            with open(p, "wb+") as file:
                file.write(s.encode('utf-8'))
                file.close()

    def __get_minimizers_multiple_path(self):
        l = list()
        l.append('CNN')
        l.append('NGG')
        l.append('NNN')
        return l

    def __write_not_full_skmer(self):
        #kmers: GUACCC,GUCCCA,GCCCAN,CCCANU,ANNCCC,ANCCCU
        path = self.__get_partitions_path("CCC", "pippo")
        part_path = self.__get_partition_file_path("pippo")
        if not os.path.exists(part_path):
            os.mkdir(part_path)
        skmer = "GUAGUAGANANUANNANU"
        with open(path,"w+b") as file:
            file.write(skmer.encode('utf-8'))
            file.close()


if __name__ == '__main__':
    unittest.main()
