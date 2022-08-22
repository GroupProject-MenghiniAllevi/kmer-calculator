import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.DSK.DefaultKmerReader import DefaultKmerReader


class MyTestCase(unittest.TestCase):


    def test_kmer_reader(self):
        file_reader = self.__initialize_file_reader()
        r = file_reader.read_next_kmer()
        l = "ACUCCGGUUG"
        self.assertEqual(l, r, " la stringa letta è: " + str(r))

    def __initialize_file_reader(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "CRW_16S_A_C_1.db")
        file_reader = DefaultKmerReader()
        file_reader.set_path(path)
        file_reader.set_kmer_lenght(10)
        return file_reader


if __name__ == '__main__':
    unittest.main()
