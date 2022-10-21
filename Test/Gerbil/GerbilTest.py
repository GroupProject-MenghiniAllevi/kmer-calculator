import os
import shutil
import unittest
from pathlib import Path

from Main.kmer.Gerbil.DefaultGerbil import DefaultGerbil
from Main.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.Reader.DefaultKmerReader import DefaultKmerReader


class GerbilTest(unittest.TestCase):

    def test_full_algorithm(self):
        self.__compute_manual_kmer()

    def test_first_phase(self):
        gerbil = DefaultGerbil(self.__get_path(), self.__get_partitions_path(), str(self.__get_output_path()), 3, 2)
        gerbil.start_first_phase_process()
        self.__check_first_phase(self.__get_partitions_path())
        self.__delete_all_partition(self.__get_partitions_path())

    def test_second_phase(self):
        self.__create_and_clean_out_file("")
        self.__write_partitions("file1", "file2")
        gerbil = DefaultGerbil(self.__get_path(), self.__get_partitions_path(), str(self.__get_output_path()), 3, 2)
        gerbil.check_molecule_lists()
        gerbil.start_second_phase_process()
        self.__check_out_file()
        s = "id,ACU,AUC,CCG,CCU,CGG,CUG,GAU,GCC,GGC,GGG,GGU,GUU,UCC,CUC,UGA,UGC,UUG\n" \
            "file1,0,5,0,6,0,9,10,1,1,5,3,23,43,33,54,2,3\n" \
            "file2,1,5,2,6,40,9,10,1,1,5,3,2,3,5,6,2,6\n"
        self.__create_and_clean_out_file(s)
        self.__write_partitions("file1", "file2")
        expected_out = "id,ACU,AUC,CCG,CCU,CGG,CUG,GAU,GCC,GGC,GGG,GGU,GUU,UCC,CUC,UGA,UGC,UUG\n" \
                       "file1,1,5,1,6,1,9,10,1,1,5,4,23,44,34,54,2,3\n" \
                       "file2,1,6,3,7,41,10,11,2,2,6,4,3,4,5,7,3,7\n"
        gerbil.start_second_phase_process()
        with open(self.__get_output_path(), "rb") as file:
            actual = file.read().decode('utf-8')
            file.close()
        self.assertEqual(expected_out, actual)
        self.__create_and_clean_out_file("")
        self.__delete_all_partition(self.__get_partitions_path())

    def __create_and_clean_out_file(self, content):
        if os.path.exists(self.__get_output_path()):
            with open(self.__get_output_path(), "wb+") as file:
                file.write(content.encode('utf-8'))
                file.close()

    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "test_algorithm")
        return path

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
                    if ic > 0 and l > 0 and l == line:
                        values.append(readed_values)
                    ic = 0
                    l += 1
                    readed_values = ""
                elif c == b"," and l > 0:
                    if ic > 0 and l == line:
                        values.append(readed_values)
                    ic += 1
                    readed_values = ""
                else:
                    readed_values += c.decode('utf-8')

        f.close()
        return values

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

    def test_large_dataset(self):
        gerbil = DefaultGerbil(os.path.abspath("D:/16S"), os.path.abspath("D:/part"), os.path.abspath("D:/out/out.csv"),
                               10, 5)
        gerbil.process()

    def __check_out_file(self):
        kmer_string = list()
        kmer_count = list()
        index_row = 0
        index_column = 0
        readed_value = ""
        with open(self.__get_output_path(), "rb") as file:
            print(file.read())
            file.close()
        with open(self.__get_output_path(), "rb") as file:
            while True:
                c = file.read(1)
                if not c:
                    break
                if c == b",":
                    if index_row == 0 and not index_column == 0:
                        kmer_string.append(str(readed_value))
                    elif index_row > 0 and not index_column == 0:
                        kmer_count.append(str(readed_value))
                    index_column += 1
                    readed_value = ""
                elif c == b"\n" or c == b"\r":
                    if index_row == 0 and not index_column == 0:
                        kmer_string.append(readed_value)
                        index_row += 1
                    elif index_row > 0 and not index_column == 0:
                        kmer_count.append(str(readed_value))
                    index_column = 0
                else:
                    readed_value += c.decode('utf-8')
            file.close()
            arr_expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                            'GGG', 'GGC', 'ACU', 'CUC', 'UCC', 'CCG', 'CGG', 'GGU']
            for i in range(len(arr_expected)):
                self.assertEqual(True, arr_expected[i] in kmer_string,
                                 "non è stato trovato l'elemento... " + arr_expected[i])

    def __get_first_phase_super_kmer_expected(self):
        CU = "AC"
        CC = "UGUUGG"
        GG = "CUCG"
        GU = "GU"
        UG = "UACC"
        AU = "GC"
        GC = "G"
        return CU, CC, GG, GU, UG, AU, GC

    def __check_first_phase(self, partition_path):
        dir_list = os.listdir(partition_path)
        self.assertTrue("file1" in dir_list)
        self.assertTrue("file2" in dir_list)
        p1_path = os.path.join(partition_path, dir_list[0])
        p2_path = os.path.join(partition_path, dir_list[1])
        files_p1 = self.__get_all_files_in_dir(p1_path)
        files_p2 = self.__get_all_files_in_dir(p2_path)
        files_p1.sort()
        files_p2.sort()
        exp_list1 = self.__get_exp_list1()
        self.__check_p_files(p1_path, files_p1, exp_list1, 3)
        exp_list2 = self.__get_exp_list2()
        self.__check_p_files(p2_path, files_p2, exp_list2, 6)

    def __compute_manual_kmer(self):
        list_of_dict = list()
        input_path = self.__get_full_sequences_input()
        dh = DefaultDirectoryHandler(input_path)
        file_list = dh.get_all_files_names()
        for file in file_list:
            d = dict()
            path_file = os.path.join(input_path, file)
            reader = DefaultKmerReader()
            reader.set_path(path_file)
            reader.set_kmer_lenght(3)
            name = reader.get_file_name()
            size = reader.get_file_lenght()
            while reader.has_next(size):
                kmer = reader.read_next_kmer()
                if kmer in d:
                    d[kmer] = d[kmer] + 1
                else:
                    d[kmer] = 1
            reader.close_file()
            list_of_dict.append(d)
            print("----------------------")
            print("name: ", name, "size:", len(d))
            d = s = dict(sorted(d.items()))
            print(d)
            print("----------------------")

    def __get_full_sequences_input(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "full_sqeunces")
        return path

    def __get_exp_list2(self):
        exp_list2 = list()
        exp_list2.append("GU")
        exp_list2.append("UACC")
        exp_list2.append("GC")
        exp_list2.append("UUGG")
        exp_list2.append("CG")
        exp_list2.append("G")
        return exp_list2

    def __get_all_files_in_dir(self, dir):
        l = list()
        for file in os.listdir(dir):
            if file.endswith(".bin"):
                l.append(file)
        return l

    def __delete_all_partition(self, partition_path):
        for filename in os.listdir(partition_path):
            file_path = os.path.join(partition_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('fallito nel cancellare %s. Reason: %s' % (file_path, e))

    def __check_p_files(self, p2_path, files_p2, exp_dict, exp_len):
        actual_list = list()
        for file in files_p2:
            p = os.path.join(p2_path, file)
            with open(p, "r+b") as ff:
                r = ff.read().decode('utf-8')
                print(r, file)
                actual_list.append(r)
                ff.close()
        self.assertEqual(exp_len, len(actual_list))
        for key in actual_list:
            self.assertTrue(key in exp_dict, key + " non è presente nel dict" + exp_dict.__str__())

    def __write_partitions(self, p1, p2):
        part_path = self.__get_partitions_path()
        file1_p = os.path.join(part_path, p1)
        file2_p = os.path.join(part_path, p2)
        if not os.path.exists(file1_p):
            os.mkdir(file1_p)
        if not os.path.exists(file2_p):
            os.mkdir(file2_p)
        d1 = dict()
        d1["GG"] = "CU"
        d1["CU"] = "AC"
        d1["CC"] = "UG"
        d2 = self.__get_dict2_file_value()
        for key in d1:
            p = os.path.join(file1_p, key + ".bin")
            self.__write_to_file(p, d1[key])
        for key in d2:
            p = os.path.join(file2_p, key + ".bin")
            self.__write_to_file(p, d2[key])

    def __get_dict2_file_value(self):
        d2 = dict()
        d2["AU"] = "GC"
        d2["CC"] = "UUGG"
        d2["GC"] = "G"
        d2["GG"] = "CG"
        d2["GU"] = "GU"
        d2["UG"] = "UACC"
        return d2

    def __write_to_file(self, path, content):
        content = content.encode('utf-8')
        if not os.path.exists(path):
            with open(path, "x") as file:
                file.close()
        with open(path, "wb+") as file:
            file.write(content)
            file.close()

    def __get_exp_list1(self):
        exp_list1 = list()
        exp_list1.append("AC")
        exp_list1.append("UG")
        exp_list1.append("CU")
        return exp_list1


if __name__ == '__main__':
    unittest.main()
