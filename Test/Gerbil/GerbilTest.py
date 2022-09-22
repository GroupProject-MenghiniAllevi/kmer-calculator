import os
import shutil
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.Gerbil.DefaultGerbil import DefaultGerbil
from it.unicam.cs.groupproject.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler


class GerbilTest(unittest.TestCase):

    def test_full_algorithm(self):
        input_path = self.__get_path()
        part_path = self.__get_partitions_path()
        out_part = self.__get_output_path()
        print(out_part)
        gerbil = DefaultGerbil(input_path, part_path, out_part, 3, 2)
        gerbil.start_first_phase_process()
        out_file = None
        try:
            out_file = open(self.__get_output_path(), "x")
            out_file.close()
        except FileExistsError:
            out_file = open(self.__get_output_path(), "w+")
            out_file.truncate()
            out_file.seek(0)
            out_file.close()
        gerbil.start_second_phase_process()
        self.__check_out_file()
        self.__delete_all_partition(self.__get_partitions_path())
    def test_first_phase(self):
        dh = DefaultDirectoryHandler(self.__get_path())
        file_list = dh.get_all_files_names()
        gerbil = DefaultGerbil(self.__get_path(), self.__get_partitions_path(), str(self.__get_output_path()), 3, 2)

        for file in file_list:
            gerbil.process_read_and_write_minimizer(self.__get_path()+"/"+file)
        self.__check_first_phase(self.__get_partitions_path())
        self.__delete_all_partition(self.__get_partitions_path())

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
        print("partition_path: ", path)
        return path

    def __get_output_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "output")
        path = os.path.join(path, "out.csv")
        return path

    def test_large_dataset(self):
        gerbil = DefaultGerbil(os.path.abspath("D:/16S"),os.path.abspath("D:/part"),os.path.abspath("D:/out/out.csv"), 10,5)
        gerbil.process()

    def __check_out_file(self):
        with open(self.__get_output_path(), "r") as f:
            lines = f.readlines()
            j = 0
            values = list()
            index = list()
            for line in lines:
                str_arr = line.split(",")
                if len(str_arr) == 2:
                    index.append(str_arr[0])
                    values.append(str_arr[1])
            arr_expected = ['GGU', 'GUU', 'UUG', 'UGA', 'GAU', 'AUC', 'UCC', 'CCU', 'CUG', 'UGC', 'GCC', 'CCG', 'CGG',
                            'GGG', 'GGC', 'ACU', 'CUC', 'UCC', 'CCG', 'CGG', 'GGU']
            for i in range(len(arr_expected)):
                self.assertEqual(True, arr_expected[i] in index, "non è stato trovato l'elemento... " + arr_expected[i])
            print(index)

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
        dh = DefaultDirectoryHandler(partition_path)
        file_list = dh.get_all_files_names()
        save_list = list()
        temp = ""
        for file in file_list:
            with open(os.path.join(partition_path, file), "r") as f:
                while True:
                    c = f.read(1)
                    if not c:
                        break
                    temp = temp + c
            save_list.append(temp)
            print("nome_file: "+file+" temp: "+temp)
            temp = ""
        expected_tuple = self.__get_first_phase_super_kmer_expected()
        for string in save_list:
            print(string)
            self.assertTrue(string in expected_tuple,"la stringa "+string+" non è nella tupla:"+str(expected_tuple))

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


if __name__ == '__main__':
    unittest.main()
