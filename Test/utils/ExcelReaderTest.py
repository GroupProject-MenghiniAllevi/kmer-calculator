import os
import unittest
from pathlib import Path

from Main.kmer.Utils.Reader.ExcelMoleculeReader import ExcelMoleculeReader


class MyTestCase(unittest.TestCase):

    def test_search_molecule_name(self):
        path = self.__get_excel_path()
        archaea_path = os.path.join(path, "Archaea.xlsx")
        reader = ExcelMoleculeReader(path=archaea_path)
        reader.extract_sheet("5S")
        name = reader.get_name_of_molecule("CRW_5S_A_C_20")
        self.assertEqual("Pyrobaculum aerophilum", str(name))
        reader.extract_sheet("16S")
        name = reader.get_name_of_molecule("CRW_16S_A_C_19")
        self.assertEqual("Pyrodictium occultum", name)

    def test_get_sheet_names(self):
        path = self.__get_excel_path()
        archaea_path = os.path.join(path, "Archaea.xlsx")
        reader = ExcelMoleculeReader(path=archaea_path)
        reader.extract_list_of_all_sheet()
        lst = reader.get_sheet_names()
        expected_list = ["5S", "16S", "23S"]
        self.assertEqual(expected_list, lst)

    def test_extract_all_names(self):
        path = self.__get_excel_path()
        archaea_path = os.path.join(path, "Archaea.xlsx")
        reader = ExcelMoleculeReader(path=archaea_path)
        reader.extract_list_of_all_sheet()
        reader.extract_all_molecule_name()
        d = reader.get_molecules()
        expected_molecules_names = self.__get_expected_names()
        for file in d:
            self.assertTrue(d[file] in expected_molecules_names)

    def __get_excel_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "excel")
        return path

    def __get_expected_names(self):
        five_s = ("Pyrobaculum aerophilum",
                  "Pyrodictium occultum",
                  "Sulfolobus acidocaldarius",
                  "Sulfolobus solfataricus",
                  "Sulfolobus sp.",
                  "Methanobacterium formicicum",
                  "Methanocaldococcus jannaschii",
                  "Methanocaldococcus jannaschii",
                  "Methanosarcina barkeri",
                  "Methanosarcina vacuolata",
                  "Methanothermus fervidus",
                  "Haloarcula marismortui",
                  "Pyrococcus woesei",
                  "Thermococcus celer",
                  "Thermoplasma acidophilum", "Halobacterium salinarum", "Halobacterium salinarum",
                  "Halococcus morrhuae",
                  "Halococcus morrhuae", "Haloferax mediterranei", "Haloferax volcanii", "Halorubrum saccharovorum",
                  "Methanolobus tindarius", "Methanothermobacter thermautotrophicus",
                  "Methanothermococcus thermolithotrophicus", "Natrialba magadii"
                  )

        sixteen_s = five_s + ("Aeropyrum pernix",
                              "Archaeoglobus fulgidus",
                              "Haloarcula marismortui rrnA",
                              "Haloarcula marismortui rrnB",
                              "Halobacterium sp. NRC-1",
                              "Haloferax volcanii",
                              "Methanobacterium formicicum",
                              "Methanococcus vannielii",
                              "Methanospirillum hungatei",
                              "Methanothermobacter thermautotrophicus",
                              "Methanothermobacter thermautotrophicus",
                              "Nanoarchaeum equitans",
                              "Natronobacterium innermongoliae",
                              "Natronorubrum bangense",
                              "Picrophilus torridus DSM 9790",
                              "Pyrococcus abyssi",
                              "Pyrococcus furiosus",
                              "Pyrococcus horikoshii",
                              "Pyrodictium occultum",
                              "Sulfolobus acidocaldarius",
                              "Sulfolobus solfataricus",
                              "Thermococcus celer",
                              "Thermoplasma acidophilum",
                              "Thermoproteus tenax",
                              )
        complete = sixteen_s + ("Haloarcula marismortui",
                                "Haloarcula marismortui rrnA",
                                "Haloarcula marismortui rrnB",
                                "Thermococcus celer",
                                )
        return complete

if __name__ == '__main__':
    unittest.main()
