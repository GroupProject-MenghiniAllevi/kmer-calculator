import os
import unittest
from pathlib import Path

from Main.kmer.Utils.Writer.OutputWriter import OutputWriter


class OutputWriterTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def test_get_new_kmer(self):
        d = dict()
        writer = OutputWriter("pippo", self.__get_out_path())
        new_kmer_values = self.__get_new_kmer()
        l = self.__get_new_kmer_index()
        self.assertEqual(l, writer.get_new_kmer_from_changed(new_kmer_values))

    def test_read_and_write_intestation(self):
        new_kmer_values = self.__get_new_kmer()
        d = dict()
        for ele in new_kmer_values:
            d[ele] = 1
        writer = OutputWriter("pippo", self.__get_out_path())
        writer.read_and_write_intestation(new_kmer_values)
        self.__check_new_out_intestation()
        new_kmer_values2 = self.__get_new_kmer_start()
        d.clear()
        for ele in new_kmer_values2:
            d[ele] = 1
        print(d)
        writer2 = OutputWriter("pluto", self.__get_out_path_2())
        writer2.read_and_write_intestation(new_kmer_values2)
        self.__check_new_out_intestation_2()

    def test_write_to_output(self):
        out_path = self.get_wto_path()
        pluto_dict = self._get_pluto_dict()
        writer = OutputWriter(filename="pluto", path=out_path)
        writer.write_to_output(pluto_dict)
        self.__check_pluto_file()

    def test_write_to_output_update_count(self):
        out_path = self.__output_writer_path()
        out_path = os.path.join(out_path, "write_to_output_update.csv")
        pippo_dict = dict()
        pippo_dict['AAA'] = 3
        writer = OutputWriter(filename="pippo", path=out_path)
        writer.write_to_output(pippo_dict)
        self.__check_pippo_file()
        pluto_dict = dict()
        pluto_dict['AGA'] = 3
        writer = OutputWriter(filename="pluto", path=out_path)
        writer.write_to_output(pluto_dict)
        self.__check_pippo_file_update()
        pippo_dict = dict()
        pippo_dict["CCC"] = 1

    def test_create_intestation(self):
        kmer_dict = self.__get_final_kmer_dict()
        writer = OutputWriter("pippo", self.__get_final_out_path())
        keys = list()
        values = list()
        for k in kmer_dict:
            values.append(kmer_dict[k])
            keys.append(k)
        writer.create_intestation(keys, len(kmer_dict), values)
        expected = self.__get_expected_new_out()
        self.__read_final_path(expected)

    def test_filename_inside_out(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "filename_test.csv")
        with open(path, "wb+") as file:
            s = "id,AAC,AAU\n" \
                "aaa,1,1\n" \
                "bbb,1,1\n" \
                "ccc,1,1\n" \
                "ddd,1,1\n" \
                "eee,1,1\n" \
                "fff,1,1\n" \
                "ggg,1,1\n"
            file.write(s.encode('utf-8'))
            file.close()
        writer = OutputWriter("pippo", path)
        actual = writer.get_all_file_names_inside_file()
        self.assertEqual(self.__get_expected_dict_filename(), actual)

    def test_k_equal_to_one(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "k_to_one.csv")
        with open(path, "wb+") as file:
            file.truncate()
            file.close()
        hash_table = self.__hash_table_k_one()
        writer = OutputWriter(filename="pippo", path=path)
        writer.write_to_output(hash_table)
        writer.close_all_files()
        expected = "id,A,C,G,N,U\npippo,2,4,8,16,32\n"
        with open(path, "rb+") as file:
            actual = file.read().decode('utf-8')
            file.truncate()
            file.close()
        self.assertEqual(expected, actual)

    def test_add_new_kmer_to_file(self):
        self.__write_file_add_kmer()  # pippo{"AAA":"1","CNN":"2","GGG":"4","GUA":"8","GUN":"16"}
        d1 = dict()  # pippo{"ACA":"5","GNC":"44","GUC":"10","GUG":"55","GUN":"2"}
        d1["ACA"] = 5
        d1["GNC"] = 44
        d1["GUC"] = 10
        d1["GUG"] = 55
        d1["GUN"] = 2
        writer = OutputWriter(filename="pippo", path=self.__get_out_path())
        writer.write_to_output(d1)
        expected_d1 = "id,AAA,ACA,CNN,GGG,GNC,GUA,GUC,GUG,GUN\n" \
                      "pippo,1,5,2,4,44,8,10,55,18\n"
        with open(self.__get_out_path(), "rb") as file:
            actual = file.read().decode('utf-8')
            file.close()
        self.assertEqual(expected_d1, actual)

    def test_add_new_molecule_to_file(self):
        s = "id,AAA,ACA,CNN,GGG,GNC,GUA,GUC,GUG,GUN,GUU\n" \
                      "pippo,1,5,2,4,44,8,10,55,18,10\n"
        with open(self.__get_out_path(),"wb+") as file:
            file.write(s.encode('utf-8'))
            file.close()
        d1 = dict()
        d1["AGA"] = 43
        expected_d1 = "id,AAA,ACA,AGA,CNN,GGG,GNC,GUA,GUC,GUG,GUN,GUU\n" \
                      "pippo,1,5,0,2,4,44,8,10,55,18,10\n" \
                      "pluto,0,0,43,0,0,0,0,0,0,0,0\n"
        writer = OutputWriter(filename="pluto",path=self.__get_out_path())
        writer.write_to_output(d1)
        with open(self.__get_out_path(),"rb") as file:
            actual = file.read().decode('utf-8')
            file.close()
        self.assertEqual(expected_d1,actual)
        with open(self.__get_out_path(),"wb+") as file:
            file.write(s.encode('utf-8'))
            file.close()

    def test_add_kmer_to_end(self):
        with open(self.__get_out_path(), "wb+") as file:
            file.write("id,AAA,ACA,CNN,GGG,GNC,GUA,GUC,GUG,GUN\n" \
                       "pippo,1,5,2,4,44,8,10,55,18\n".encode('utf-8'))
            file.close()
        d2 = dict()
        d2["GUU"] = 10
        writer = OutputWriter(filename="pippo", path=self.__get_out_path())
        writer.write_to_output(d2)
        expected_d2 = "id,AAA,ACA,CNN,GGG,GNC,GUA,GUC,GUG,GUN,GUU\n" \
                      "pippo,1,5,2,4,44,8,10,55,18,10\n"
        with open(self.__get_out_path(), "rb") as file:
            actual = file.read().decode('utf-8')
            file.close()
        self.assertEqual(expected_d2, actual)
        with open(self.__get_out_path(), "wb+") as file:
            file.write("id,AAA,AUA,CAU,CCC,CCU,GGG\npippo,1,2,3,1,1,0\n".encode('utf-8'))
            file.close()

    def test_add_kmer_to_k_one(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "k_to_one.csv")
        with open(path, "wb+") as file:
            file.truncate()
            s = "id,A,C,G,N,U\npippo,2,4,8,16,32\n"
            file.write(s.encode('utf-8'))
            file.close()
        d = self.__get_dict_k_two()
        writer = OutputWriter(filename="pluto", path=path)
        writer.write_to_output(d)
        writer.close_all_files()
        expected = "id,A,C,G,N,U,AA,CC,GG,NN,UU\npippo,2,4,8,16,32,0,0,0,0,0\npluto,0,0,0,0,0,2,4,8,16,32\n"
        with open(path, "r+b") as file:
            actual = file.read().decode('utf-8')
            file.truncate()
            file.close()
        self.assertEqual(expected, actual)

    def test_add_different_kmer_len(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "k_to_one.csv")
        with open(path, "wb+") as file:
            file.truncate()
            s = "id,A,C,G,N,U,AA,CC,GG,NN,UU\npippo,2,4,8,16,32,0,0,0,0,0\npluto,0,0,0,0,0,2,4,8,16,32\n"
            file.write(s.encode('utf-8'))
            file.close()
        d = dict()
        d['GN'] = 10
        writer = OutputWriter(filename="pluto", path=path)
        writer.write_to_output(d)
        writer.close_all_files()
        expected = "id,A,C,G,N,U,AA,CC,GG,GN,NN,UU\npippo,2,4,8,16,32,0,0,0,0,0,0\npluto,0,0,0,0,0,2,4,8,10,16,32\n"
        with open(path, "r+b") as file:
            actual = file.read().decode('utf-8')
            file.truncate()
            file.close()
        self.assertEqual(expected, actual)

    def __get_changed_values_actual(self):
        return [['AAA', 'AUA', 'CCU'], ['CAU', 'CCC', 'AAU']]

    def __get_changed_values_dictionary(self):
        d1 = dict()
        d2 = dict()
        d1['AAA'] = 1
        d1['AUA'] = 2
        d2['CAU'] = 3
        d2['CCC'] = 1
        d1['CCU'] = 1
        d2['GGG'] = 1
        return d1, d2

    def __expected_changed_index(self):
        return [[1, 2, 5], [3, 4, 6]]

    def __get_keys_changed(self):
        return self.__get_changed_values_dictionary()[0].keys(), self.__get_changed_values_dictionary()[1].keys()

    def __expected_dict_changed_value(self):
        d1 = dict()
        d1[1] = 1
        d1[2] = 2
        d1[5] = 1
        d2 = dict()
        d2[3] = 3
        d2[4] = 1
        d2[6] = 0
        return d1, d2

    def __get_out_path(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "out.csv")
        return path

    def __output_writer_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "OutputWriter")
        return path

    def __get_index_of_changed_value(self):
        return [[1, 2, 5], [3, 4, 6]]

    def __get_new_kmer(self):
        l = list()
        l.append("ACA")
        l.append("AUA")
        l.append("AUC")
        l.append("UUU")
        return l

    def __check_new_out_intestation(self):
        new_out_path = self.__get_new_out_path()
        with open(new_out_path, "r") as f:
            line = f.readline()
            f.close()
        self.assertEqual("id,AAA,ACA,AUA,AUC,CAU,CCC,CCU,GGG,UUU\n", line,
                         "la linea scritta sul nuovo file è: " + line)
        os.remove(new_out_path)

    def __get_new_out_path(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "new_out.csv")
        return path

    def __get_new_kmer_index(self):
        l = list()
        l.append("ACA")
        l.append('AUC')
        l.append('UUU')
        return l

    def __get_out_path_2(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "out2.csv")
        return path

    def __check_new_out_intestation_2(self):
        new_out_path = self.__get_new_out_path()
        with open(new_out_path, "r") as f:
            line = f.readline()
            f.close()
        self.assertEqual("id,AAA,AAC,CAC,CAG,UUU\n", line,
                         "la linea scritta sul nuovo file è: " + line)
        os.remove(new_out_path)

    def __get_new_kmer_start(self):
        l = list()
        l.append('AAA')
        l.append("AAC")
        return l

    def __get_final_out_path(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "final_out.csv")
        return path

    def __get_final_kmer_dict(self):
        d = dict()
        d['AGU'] = 1
        d['AUA'] = 3
        d['CUU'] = 2
        return d

    def __get_expected_new_out(self):
        return "id,AGU,AUA,CUU\npippo,1,3,2\n"

    def __read_final_path(self, expected):
        r = ""
        with open(self.__get_new_out_path(), "rb") as f:
            r = f.read().decode()
        self.assertEqual(expected, r, "la linea letta è: " + r)

    def get_wto_path(self):
        path = self.__output_writer_path()
        path = os.path.join(path, "write_to_output.csv")
        return path

    def _get_pluto_dict(self):
        l = dict()
        l['AAA'] = 1
        l['AGA'] = 1
        l['UUU'] = 3
        return l

    def __check_pluto_file(self):
        with open(self.get_wto_path(), "rb") as file:
            line = file.read()
            file.close()
        self.assertEqual(self.__get_expected_pluto(), line.decode(encoding='utf-8'))
        with open(self.get_wto_path(), "wb+") as file:
            s = "id,AAU,ACA,ACG,ACU,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU\npippo,1,1,1,1,1,1,1,1,1,2,2,2,2,5\n"
            file.write(s.encode('utf-8'))
            file.close()

    def __get_expected_pluto(self):
        return "id,AAA,AAU,ACA,ACG,ACU,AGA,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU,UUU\npippo,0,1,1,1,1,0,1,1,1,1,1," \
               "2,2,2,2,5,0\npluto,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,3\n"

    def __get_expected_dict_filename(self):
        d = dict()
        d["aaa"] = 11
        d["bbb"] = 19
        d["ccc"] = 27
        d["ddd"] = 35
        d["eee"] = 43
        d["fff"] = 51
        d["ggg"] = 59
        return d

    def __get_expected_pippo(self):
        return "id,AAA,AAU,ACA,ACG,ACU,AGA,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU,UUU\npippo,3,1,1,1,1,0,1,1,1,1,1," \
               "2,2,2,2,5,0\npluto,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,3\n"

    def __check_pippo_file(self):
        path = os.path.join(self.__output_writer_path(), "write_to_output_update.csv")
        with open(path, "rb") as file:
            line = file.read()
            file.close()
        self.assertEqual(self.__get_expected_pippo(), line.decode(encoding='utf-8'))
        with open(path, "wb+") as file:
            s = "id,AAA,AAU,ACA,ACG,ACU,AGA,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU,UUU\n" \
                "pippo,0,1,1,1,1,0,1,1,1,1,1,2,2,2,2,5,0\n" \
                "pluto,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,3\n"
            file.write(s.encode('utf-8'))
            file.close()

    def __check_pippo_file_update(self):
        path = os.path.join(self.__output_writer_path(), "write_to_output_update.csv")
        with open(path, "rb") as file:
            line = file.read()
            file.close()
        self.assertEqual(self.__get_expected_pippo_update(), line.decode(encoding='utf-8'))
        with open(path, "wb+") as file:
            s = "id,AAA,AAU,ACA,ACG,ACU,AGA,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU,UUU\n" \
                "pippo,0,1,1,1,1,0,1,1,1,1,1,2,2,2,2,5,0\n" \
                "pluto,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,3\n"
            file.write(s.encode('utf-8'))
            file.close()

    def __get_expected_pippo_update(self):
        return "id,AAA,AAU,ACA,ACG,ACU,AGA,AGG,AUU,CAA,CCU,CGG,CGU,GGU,UAA,UCU,UGU,UUU\npippo,0,1,1,1,1,0,1,1,1,1,1," \
               "2,2,2,2,5,0\npluto,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,3\n"

    def __hash_table_k_one(self):
        d = dict()
        d['A'] = 2
        d['C'] = 4
        d['G'] = 8
        d['N'] = 16
        d['U'] = 32
        return d

    def __get_dict_k_two(self):
        d = dict()
        d['AA'] = 2
        d['CC'] = 4
        d['GG'] = 8
        d['NN'] = 16
        d['UU'] = 32
        return d

    def __check_new_out_intestation_not_sorted(self):
        new_out_path = self.__get_new_out_path()
        with open(new_out_path, "r") as f:
            line = f.readline()
            f.close()
        self.assertEqual("id,AAN,CAC,CAG,GGG,UUU\n", line,
                         "la linea scritta sul nuovo file è: " + line)
        os.remove(new_out_path)
        pass

    def __write_file_add_kmer(self):
        out_path = self.__get_out_path()
        content = "id,AAA,CNN,GGG,GUA,GUN\npippo,1,2,4,8,16\n"
        with open(out_path, "wb+") as file:
            file.write(content.encode('utf-8'))
            file.close()
