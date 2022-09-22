import os
import shutil
import unittest
from pathlib import Path
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKAlgorithm import DefaultDskAlgorithm


class DSKAlgorithmTest(unittest.TestCase):

    def test_create_partition(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        p = self.__get_partition_files()
        p_sub = self.__get_partition_sub_folders()
        dsk_algorithm.create_partition_files(p_sub[0], 1)
        dsk_algorithm.create_partition_files(p_sub[1], 1)
        self.assertTrue(os.path.isdir)
        self.assertTrue(os.path.isdir)
        self.assertTrue(os.path.isfile(p[0]))
        self.assertTrue(os.path.isfile(p[1]))
        shutil.rmtree(p_sub[0])
        shutil.rmtree(p_sub[1])

    def __get_partition_sub_folders(self):
        path1 = os.path.join(self.__get_partitions_path(), "file1")
        path2 = os.path.join(self.__get_partitions_path(), "file2")
        return path1, path2

    def test_save_to_partition(self):
        dsk_algorithm = self.__get_dsk_algorithm()
        p = self.__get_partition_files()
        p_sub = self.__get_partition_sub_folders()
        dsk_algorithm.create_partition_files(p_sub[0], 1)
        dsk_algorithm.create_partition_files(p_sub[1], 1)
        dsk_algorithm.save_to_partitions(0, 1, 1, "file1.db")
        self.__check_saves_first_file(p[0])
        dsk_algorithm.save_to_partitions(0, 1, 1, "file2.db")
        self.__check_saves_second_file(p[1])
        path1 = os.path.join(self.__get_partitions_path(), "file1")
        path2 = os.path.join(self.__get_partitions_path(), "file2")
        # shutil.rmtree(path1)
        # shutil.rmtree(path2)

    def __get_partition_file_path(self):
        return Path(os.path.join(self.__get_partitions_path(), "partition-0.bin")), Path(
            os.path.join(self.__get_partitions_path(), "partition-1.bin"))

    def __get_partition_files(self):
        # file1 = k_numb : 6, ith : 1, part : 1
        # file2 = k_numb : 15, ith : 1, part : 1
        path1 = os.path.join(self.__get_partitions_path(), "file1")
        path1 = os.path.join(path1, "partition-0.bin")
        path2 = os.path.join(self.__get_partitions_path(), "file2")
        path2 = os.path.join(path2, "partition-0.bin")
        return path1, path2

    def __get_dsk_algorithm(self):
        dsk_algorithm = DefaultDskAlgorithm(3, 1024, 1024, self.__get_path(), self.__get_partitions_path())
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
        dsk_algorithm.thread_partitions_write("file1.db", 0)
        dsk_algorithm.thread_partitions_write("file2.db", 0)
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
                    app1 = app.decode('utf-8')
                    bb = str(app1) + bb
        return bb

    def test_full_algorithm(self):
        dsk_algorithm = self.__get_full_dsk()
        dsk_algorithm.process(self.__get_partitions_path(), self.__get_output_path())
        self.__check_out_file()

    def __check_out_file(self):
        with open(self.__get_output_path(), "rb") as file:
            values = list()
            index = list()
            readed_value = ""
            while True:
                c = file.read(1)
                if not c or c == b"\n" or c == b"\r":
                    index.append(readed_value)
                    readed_value = ""
                    break
                else:
                    if c == b",":
                        index.append(readed_value)
                        readed_value = ""
                    else:
                        readed_value += c.decode('utf-8')
            arr_expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                            'GGG', 'GGC', 'ACU', 'CUC', 'UCC', 'CCG', 'CGG', 'GGU']
            file.close()
        arr_expected.sort()
        first_line = self.__get_valeus_from_file(1)
        second_line = self.__get_valeus_from_file(2)
        for i in range(len(arr_expected)):
                self.assertEqual(True, arr_expected[i] in index, "non è stato trovato l'elemento... " + arr_expected[i])
        ex_l1 = ['1','0','1','0','1','0','0','0','0','0','1','0','1','1','0','0','0']
        ex_l2 = ['0','1','1','1','1','1','1','1','1','1','1','1','1','0','1','1','1']
        self.assertEqual(ex_l1,first_line)
        self.assertEqual(ex_l2,second_line)

    def __get_full_dsk(self):
        dsk_algorithm = DefaultDskAlgorithm(3, 128, 128, self.__get_path(), self.__get_partitions_path())
        dsk_algorithm.set_iteration_number()
        dsk_algorithm.set_partition_number()
        return dsk_algorithm

    def __check_saves_first_file(self, path):
        list_of_kmer = list()
        with open(path, "rb") as f:
            while True:
                c = f.read(3)
                if not c:
                    break
                else:
                    list_of_kmer.append(c.decode("utf-8"))
        expected = ["ACU", "CUC", "UCC", "CCG", "CGG", "GGU"]
        self.assertEqual(len(expected), len(list_of_kmer))
        for e in expected:
            self.assertTrue(e in list_of_kmer)

    def __check_saves_second_file(self, path):
        list_of_kmer = list()
        with open(path, "rb") as f:
            while True:
                c = f.read(3)
                if not c:
                    break
                else:
                    list_of_kmer.append(c.decode("utf-8"))
        expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                    'GGG', 'GGC']
        self.assertEqual(len(expected), len(list_of_kmer))
        for e in expected:
            self.assertTrue(e in list_of_kmer)

    def __get_valeus_from_file(self, line):
        f = open(self.__get_output_path(), "rb")
        l = 0
        ic = 0
        values = list()
        readed_values = ""
        while True:
            c = f.read(1)
            if not c or l > line:
                break
            else:
                if c == b"\n" or c == b"\r":
                    if ic > 0 and l>0 and l == line:
                        values.append(readed_values)
                    ic = 0
                    l += 1
                    readed_values = ""
                elif c == b"," and l>0:
                    if ic > 0 and l == line:
                        values.append(readed_values)
                    ic += 1
                    readed_values =""
                else:
                    readed_values += c.decode('utf-8')

        f.close()
        return values


if __name__ == '__main__':
    unittest.main()
