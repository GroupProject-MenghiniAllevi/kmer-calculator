import os
import shutil
import unittest
from pathlib import Path

from Main.kmer.KMC3.DefaultKMC3 import DefaultKMC3


class MyTestCase(unittest.TestCase):

    def test_check_file_list(self):
        kmc3 = DefaultKMC3(self.__get_input_path(), self.__get_partition_path(), self.__get_output_path(), 3, 2)
        input_file_list = kmc3.extract_file_list()
        expected_file_list = ("file1.db", "file2.db")
        for i in input_file_list:
            self.assertTrue(i in expected_file_list)

    def test_create_partition_sub_folder(self):
        kmc3 = DefaultKMC3(self.__get_input_path(), self.__get_partition_path(), self.__get_output_path(), 3, 2)
        input_file_list = kmc3.extract_file_list()
        kmc3.create_partitions(self.__get_partition_path(), input_file_list)
        exp_path_file_1 = os.path.join(self.__get_partition_path(), "file1.db")
        exp_path_file_2 = os.path.join(self.__get_partition_path(), "file2.db")
        self.assertTrue(os.path.exists(exp_path_file_1))
        self.assertTrue(os.path.exists(exp_path_file_2))
        shutil.rmtree(exp_path_file_1)
        shutil.rmtree(exp_path_file_2)

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

    def test_phase_one(self):
        kmc3 = DefaultKMC3(self.__get_input_path(), self.__get_partition_path(), self.__get_output_path(), 3, 2)
        input_file_list = kmc3.extract_file_list()
        kmc3.create_partitions(self.__get_partition_path(), input_file_list)
        kmc3.extract_molecule_name()
        for file in input_file_list:
            input_file_path = os.path.join(self.__get_input_path(), file)
            partition_path = os.path.join(self.__get_partition_path(), file)
            kmc3.write_kmer_to_partition(partition_path, input_file_path)
        self.__check_first_phase(self.__get_partition_path())
        self.__delete_all_partition(self.__get_partition_path())

    def test_second_phase(self):
        self.__create_and_clean_out_file("")
        kmc3 = DefaultKMC3(self.__get_input_path(), self.__get_partition_path(), self.__get_output_path(), 3, 2)
        input_file_list = kmc3.extract_file_list()
        kmc3.create_partitions(self.__get_partition_path(), input_file_list)
        p1, p2 = self.__write_partitions("file1.db", "file2.db")
        l = list()
        l.append(p1)
        l.append(p2)
        kmc3.extract_molecule_name()
        for file in l:
            kmc3.read_skmer_and_print_to_output(file)
        self.__check_out_file()

    def __check_out_file(self):
        kmer_string = list()
        kmer_count1 = list()
        kmer_count2 = list()
        index_row = 0
        index_column = 0
        readed_value = ""
        with open(self.__get_output_path(), "rb") as file:
            while True:
                c = file.read(1)
                if not c:
                    break
                if c == b",":
                    if index_row == 0 and not index_column == 0:
                        kmer_string.append(str(readed_value))
                    elif index_row > 0 and not index_column == 0:
                        if index_row == 2:
                            kmer_count1.append(str(readed_value))
                        else:
                            kmer_count2.append(str(readed_value))
                    index_column += 1
                    readed_value = ""
                elif c == b"\n" or c == b"\r":
                    if index_row == 0 and not index_column == 0:
                        kmer_string.append(readed_value)
                        index_row += 1
                    elif index_row > 0 and not index_column == 0:
                        if index_row == 2:
                            kmer_count1.append(str(readed_value))
                        else:
                            kmer_count2.append(str(readed_value))
                    index_column = 0
                    index_row+=1
                else:
                    readed_value += c.decode('utf-8')
            file.close()
            arr_expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                            'GGG', 'GGC', 'ACU', 'CUC', 'UCC', 'CCG', 'CGG', 'GGU']
            for i in range(len(arr_expected)):
                self.assertEqual(True, arr_expected[i] in kmer_string,
                                 "non è stato trovato l'elemento... " + arr_expected[i])
            ex_l1 = ['1', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0']
            ex_l2 = ['0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            self.assertEqual(ex_l1,kmer_count1)
            self.assertEqual(ex_l2,kmer_count2)

    def __check_first_phase(self, partition_path):
        dir_list = os.listdir(partition_path)
        self.assertTrue("file1.db" in dir_list)
        self.assertTrue("file2.db" in dir_list)
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

    def __create_and_clean_out_file(self, content):
        if os.path.exists(self.__get_output_path()):
            with open(self.__get_output_path(), "wb+") as file:
                if not content == "":
                    file.write(content.encode('utf-8'))
                file.close()

    def __check_p_files(self, p2_path, files_p2, exp_dict, exp_len):
        actual_list = list()
        for file in files_p2:
            p = os.path.join(p2_path, file)
            with open(p, "r+b") as ff:
                r = ff.read().decode('utf-8')
                actual_list.append(r)
                ff.close()
        self.assertEqual(exp_len, len(actual_list))
        for key in actual_list:
            self.assertTrue(key in exp_dict, key + " non è presente nel dict" + exp_dict.__str__())

    def __get_exp_list1(self):
        exp_list1 = list()
        exp_list1.append("AC")
        exp_list1.append("UG")
        exp_list1.append("CU")
        return exp_list1

    def __get_exp_list2(self):
        exp_list2 = list()
        exp_list2.append("GU")
        exp_list2.append("UACC")
        exp_list2.append("GC")
        exp_list2.append("UUGG")
        exp_list2.append("CG")
        exp_list2.append("G")
        return exp_list2

    def __get_exp_dict2(self):
        d2 = dict()
        d2["AU"] = "GC"
        d2["CC"] = "UUGG"
        d2["GC"] = "G"
        d2["GG"] = "CG"
        d2["GU"] = "GU"
        d2["UG"] = "UACC"
        return d2

    def __get_all_files_in_dir(self, dir):
        l = list()
        for file in os.listdir(dir):
            if file.endswith(".bin"):
                l.append(file)
        return l

    def __get_input_path(self):
        mp = self.__get_main_path()
        path = os.path.join(mp, "test_algorithm")
        return path

    def __get_main_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        return path

    def __get_partition_path(self):
        mp = self.__get_main_path()
        path = os.path.join(mp, "partitions")
        return path

    def __get_output_path(self):
        mp = self.__get_main_path()
        path = os.path.join(mp, "output")
        path = os.path.join(path, "out.csv")
        return path

    def __write_partitions(self, p1, p2):
        part_path = self.__get_partition_path()
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
        d2 = self.__get_exp_dict2()
        for key in d1:
            p = os.path.join(file1_p, key + ".bin")
            self.__write_to_file(p, d1[key])
        for key in d2:
            p = os.path.join(file2_p, key + ".bin")
            self.__write_to_file(p, d2[key])
        return file1_p, file2_p

    def __write_to_file(self, path, content):
        content = content.encode('utf-8')
        if not os.path.exists(path):
            with open(path, "x") as file:
                file.close()
        with open(path, "wb+") as file:
            file.write(content)
            file.close()


if __name__ == '__main__':
    unittest.main()
