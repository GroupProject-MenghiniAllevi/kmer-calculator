import unittest

from Main.kmer.Utils.minimizer.DefaultMinimizer import DefaultMinimizer


class MinimizersTest(unittest.TestCase):
    def test_minimizers_add(self):
        minimizer = self.__get_minimizer()
        l = self.get_list_string()
        self.__apply_add(minimizer,l)
        self.assertEqual("ACUCCUCCUCCACCACCACA",self.__from_bytes_to_string(minimizer))

    def __apply_add(self,minimizer,l):
        for s in l:
            minimizer.add_kmer_without_minimizer(s)
        return minimizer

    def test_complex_minimizer(self):
        minimizer = self.__get_minimizer()
        l = self.get_complex_list_string()
        minimizer = self.__apply_add(minimizer,l)
        self.assertEqual("ACUCCUCCUCCACCACCACAACUCCUCCUCCACCACCACA",self.__from_bytes_to_string(minimizer))




    def __from_bytes_to_string(self,minimizer):
        actual = ""
        for s in minimizer.get_super_kmer():
            actual = actual + bytes.decode(s,"UTF-8")
        return actual

    def __get_minimizer(self):
        minimizer = DefaultMinimizer(4)
        minimizer.set_minimizers("CUGU")
        return minimizer


    def get_list_string(self):
        l = list()
        l.append("ACUCCUGU")
        l.append("CUCCUGUC")
        l.append("UCCUGUCA")
        l.append("CCUGUCAC")
        l.append("CUGUCACA")
        return l

    def get_complex_list_string(self):
        l = self.get_list_string()
        l.append("ACUCCUGU")
        l.append("CUCCUGUC")
        l.append("UCCUGUCA")
        l.append("CCUGUCAC")
        l.append("CUGUCACA")
        return l


if __name__ == '__main__':
    unittest.main()
