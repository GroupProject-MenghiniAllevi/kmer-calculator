import unittest

from Main.kmer.Utils.MostSignificantRadixSort import MostSignificantRadixSort


class MyTestCase(unittest.TestCase):

    def test_get_list(self):
        l = ["AAC", "CCA", "NUU"]
        radix_sort = MostSignificantRadixSort(l)
        actual = radix_sort.get_list()
        self.assertEqual(l, actual)

    def test_sort_list(self):
        self.__test_first_list()
        self.__test_second_list()

    def __test_first_list(self):
        l = ["CCA", "NUU", "AAC"]
        l1 = l
        l1.sort()
        radix_sort = MostSignificantRadixSort(l)
        radix_sort.sort()
        self.assertEqual(["AAC", "CCA", "NUU"], radix_sort.get_list())

    def __test_second_list(self):
        l1 = ["UUN", "NGA", "AAA", "CCC"]
        s = MostSignificantRadixSort(l1)
        s.sort()
        self.assertEqual(["AAA", "CCC", "NGA", "UUN"], s.get_list())


if __name__ == '__main__':
    unittest.main()
