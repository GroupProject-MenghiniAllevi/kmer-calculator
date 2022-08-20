import unittest
from it.unicam.cs.groupproject.kmer.DSK.DefaultDirectoryHandler import DefaultDirectoryHandler


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_file_lenght(self):
        path = ""
        dh = DefaultDirectoryHandler(path="")



if __name__ == '__main__':
    unittest.main()
