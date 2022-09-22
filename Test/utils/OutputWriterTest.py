import os
import unittest
from pathlib import Path

from it.unicam.cs.groupproject.kmer.Utils.OutputWriter import OutputWriter


class OutputWriterTest(unittest.TestCase):

    def test_get_new_kmer(self):
        writer = OutputWriter("pippo", self.__get_out_path())
        kmer_keys = self.__get_changed_values_actual()
        new_kmer_values = self.__get_new_kmer()
        l = self.__get_new_kmer_index()
        self.assertEqual(l, writer.get_new_kmer_from_changed(new_kmer_values))

    def test_read_and_write_intestation(self):
        new_kmer_values = self.__get_new_kmer()
        writer = OutputWriter("pippo", self.__get_out_path())
        writer.read_and_write_intestation(new_kmer_values)
        self.__check_new_out_intestation()
        writer2 = OutputWriter("pluto", self.__get_out_path_2())
        new_kmer_values = self.__get_new_kmer_start()
        writer2.read_and_write_intestation(new_kmer_values)
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
        writer = OutputWriter(filename="pippo", path=out_path)
        pippo_dict = dict()
        pippo_dict['AAA'] = 3
        writer.write_to_output(pippo_dict)
        self.__check_pippo_file()
        writer = OutputWriter(filename="pluto", path=out_path)
        pluto_dict = dict()
        pluto_dict['AGA'] = 3
        writer.write_to_output(pluto_dict)
        self.__check_pippo_file_update()

    def test_create_intestation(self):
        writer = OutputWriter("pippo", self.__get_final_out_path())
        kmer_dict = self.__get_final_kmer_dict()
        keys = list()
        values = list()
        for k in kmer_dict:
            values.append(kmer_dict[k])
            keys.append(k)
        writer.create_intestation(keys, len(keys), values)
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
        writer = OutputWriter("otto", path)
        actual = writer.get_all_file_names_inside_file()
        self.assertEqual(self.__get_expected_dict_filename(), actual)

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
