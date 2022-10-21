import os
import unittest
from pathlib import Path

from Main.kmer.simplekmercounter.SimpleKmerCounter import SimpleKmerCounter


class MyTestCase(unittest.TestCase):

    def test_kmer_count(self):
        self.__write_input_files()
        self.__clear_output_path(self.__get_out_path())
        path = self.__get_path()
        kmer_count = SimpleKmerCounter(path,3)
        kmer_count.process(self.__get_out_path())
        self.__check_out_file(self.__get_out_path(),"id,ACU,AUC,CCG,CCU,CGG,CUC,CUG,GAU,GCC,GGC,GGG,GGU,GUU,UCC,UGA,"
                                                    "UGC,UUG\nfile1,1,0,1,0,1,1,0,0,0,0,0,1,0,1,0,0,0\nfile2,0,1,1,1,"
                                                    "1,0,1,1,1,1,1,1,1,1,1,1,1\n")


    def __get_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "test_algorithm")
        return path

    def __get_out_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "output")
        path = os.path.join(path, "out.csv")
        return path

    def __check_out_file(self, out_path,expected):
        with open(out_path,"rb") as file:
            actual = file.read().decode('utf-8')
            file.close()
        self.assertEqual(expected, actual)

    def __clear_output_path(self, path):
        if not os.path.exists(path):
            with open(path,"x") as file:
                file.close()
        else:
            with open(path, "wb+") as file:
                file.close()

    def __write_input_files(self):
        f1 = os.path.join(self.__get_path(),"file1.db")
        f2 = os.path.join(self.__get_path(),"file2.db")
        with open(f1,"wb+")as file:
            s = "name: file1\nL\nL\nL\nACUCCGGU\n"
            file.write(s.encode('utf-8'))
            file.close()
        with open(f2,"wb+")as file:
            s = "name: file2\nL\nL\nL\nGGUUGAUCCUGCCGGGC\n"
            file.write(s.encode('utf-8'))
            file.close()

if __name__ == '__main__':
    unittest.main()
