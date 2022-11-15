import os.path
from Main.FeaturesSelection.FSelector import FSelector
from Main.kmer.DSK.DefaultDSKAlgorithm import DefaultDskAlgorithm
from Main.kmer.Gerbil.DefaultGerbil import DefaultGerbil
from Main.kmer.KMC3.DefaultKMC3 import DefaultKMC3
from Main.kmer.simplekmercounter.SimpleKmerCounter import SimpleKmerCounter


class CLIView:
    __argc = 0
    __argv = []
    __mode = ""
    __try_call = 0
    def __init__(self, argc, argv, mode: str = "kmerCalculator"):
        self.__argv = argv
        self.__argc = argc
        self.__mode = mode


    def check_if_is_help(self):
        self.__try_call += 1
        if self.__argc == 2 and self.__argv[1] == '-h':
            print("Questo programma serve per calcolare i kmer delle sequenze di rna in formato dot bracket da 1 a k "
                  "di una lista di file.\n"
                  "L'alfabeto accettato nelle sequenze è quello presente su "
                  "https://www.bioinformatics.org/sms/iupac.html.\n "
                  "Utilizzo: -n <nome_algoritmo> -input <percorso_cartella_file_input> -part <percorso_partizioni> "
                  "-out <percorso_file_output> -k <dimensione_massima_kmer>\n"
                  "Gli algoritmi disponibili sono 3:\n"
                  "     gerbil\n"
                  "     kmc3\n"
                  "     dsk\n")

    def check_if_is_DSK(self):
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "dsk":
            input_path = self.__argv[4]
            part = self.__argv[6]
            output = self.__argv[8]
            k = int(self.__argv[10])
            with open(output, "wb+") as ff:
                ff.truncate()
                ff.close()
            k_index = 1
            while k_index <= k:
                print("calcolando i kmer per k == " + str(k_index))
                dsk = DefaultDskAlgorithm(k_index, 81920, 81920, input_path, part)
                dsk.set_iteration_number()
                dsk.set_partition_number()
                dsk.process(output)
                k_index += 1

    def check_if_is_gerbil(self):
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "gerbil":
            input_path = self.__argv[4]
            part = self.__argv[6]
            output = self.__argv[8]
            k = int(self.__argv[10])
            k_index = 1
            if os.path.exists(output):
                with open(output, "wb+") as ff:
                    ff.truncate()
                    ff.close()
            else:
                with open(output, "x") as ff:
                    ff.truncate()
                    ff.close()
            while k_index <= k:
                print("eseguendo il calcolo per k == " + str(k_index))
                if k_index == 1:
                    kmer_count = SimpleKmerCounter(input_path, 1)
                    kmer_count.process(output)
                else:
                    min_size = k_index - 1
                    gerbil = DefaultGerbil(input_path, part, output, k_index, min_size)
                    gerbil.process()
                k_index += 1

    # -n kmc3 -input percorso/cartella/input/ -part percorso/cartella/partizioni/ -out percorso/file/output -k [
    # lunghezza massima dei kmer]
    def check_if_is_kmc3(self):
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "kmc3":
            input_path = self.__argv[4]
            part = self.__argv[6]
            output = self.__argv[8]
            k = int(self.__argv[10])
            k_index = 1
            if os.path.exists(output):
                with open(output, "wb+") as ff:
                    ff.truncate()
                    ff.close()
            else:
                with open(output, "x") as ff:
                    ff.truncate()
                    ff.close()
            while k_index <= k:
                print("eseguendo il calcolo per k == " + str(k_index))
                if not k_index == 1:
                    min_size = k_index - 1
                    kmc3 = DefaultKMC3(input_path, part, output, k_index, min_size)
                    kmc3.process()
                else:
                    kmer_count = SimpleKmerCounter(input_path, 1)
                    print(kmer_count.detect_molecule_name_from_input())
                    kmer_count.process(output)
                k_index += 1

    def check_if_is_low_variance(self):  # -n features_selection -m low_variance path/input/file path/output/file
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__argv[3] == "-m" and self.__argv[
            4] == "low_variance":
            self.__check_if_input_output_empty()
            selector = FSelector(self.__argv[5])
            selector.apply_low_variance(threshold=(.8 * (1 - .8)))
            selector.write_to_output(self.__argv[6])

    # main -n features_selection -m l1_based path/input/file path/output/file
    def check_if_is_L1_based_selection(self):
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__mode == "featuresSelction":
            if self.__argv[3] == "-m" and self.__argv[4] == "l1_based":
                self.__check_if_input_output_empty()
                selector = FSelector(self.__argv[5], supervised=True)
                selector.apply_L1_based()
                selector.write_to_output(self.__argv[6])

    # main -n features_selection -m sfs_forward path/input/file path/output/file
    def check_if_is_sequential_features_selection(self):
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__mode == "featuresSelction":
            if self.__argv[3] == "-m" and self.__argv[4] == "sfs_forward":
                self.__check_if_input_output_empty()
                selector = FSelector(self.__argv[5], supervised=True)
                selector.apply_Sequential_features_selection()
                selector.write_to_output(self.__argv[6])

    # main -n features_selection -m rtree path/input/file path/output/file
    def check_if_is_recursive_tree_features_selection(self):
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__mode == "featuresSelction":
            if self.__argv[3] == "-m" and self.__argv[4] == "tree":
                self.__check_if_input_output_empty()
                selector = FSelector(self.__argv[5], supervised=True)
                selector.apply_recursive_tree()
                selector.write_to_output(self.__argv[6])

    def __check_if_input_output_empty(self):
        if self.__argv[5] == "" or self.__argv[6] == "":
            raise ValueError("comando errato. il programma accetta questo comando:\n"
                             "-n features_selection -m low_variance path/input/file path/output/file")

    # main -n features_selection -m chi2 path/input/file path/output/file
    def check_if_is_chi2(self):
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection":
            if self.__argv[3] == "-m" and self.__argv[4] == "chi2":
                self.__check_if_input_output_empty()
                selector = FSelector(self.__argv[5], supervised=True)
                selector.apply_chi2_test()
                selector.write_to_output(self.__argv[6])

    # main -n features_selection -m threeFS path/input/file path/output/file
    def check_if_is_three_FS(self):
        self.__try_call += 1
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__mode == "featuresSelction":
            if self.__argv[3] == "-m" and self.__argv[4] == "threeFS":
                self.__check_if_input_output_empty()
                parent_path = os.path.dirname(self.__argv[6])
                f1_path = os.path.join(parent_path, "f1.csv")
                f2_path = os.path.join(parent_path, "f2.csv")
                selector = FSelector(self.__argv[5])
                selector.apply_low_variance(threshold=(.9 * (1 - .9)))
                selector.write_to_output(f1_path)
                selector1 = FSelector(f1_path, supervised=True)
                selector1.apply_L1_based()
                selector1.write_to_output(f2_path)
                selector2 = FSelector(f2_path, supervised=True)
                selector2.apply_chi2_test()
                selector2.write_to_output(self.__argv[6])

    def check_if_is_rand_log_reg(self):
        self.__try_call +=1
        if self.__argv[1] == "-n" and self.__argv[2] == "features_selection" and self.__mode == "featuresSelction":
            if self.__argv[3] == "-m" and self.__argv[4] == "rlr":
                self.__check_if_input_output_empty()
                selector = FSelector(self.__argv[5])
                selector.rlr()
                selector.write_to_output(self.__argv[6])

    def check_right_command(self):
        if self.__mode == "featuresSelction" and self.__try_call == 4:
            print("Il comando corretto e':\n"
                  "python FeaturesSelection.py -n <features_selection> -m <metodo-scelto> <file/csv/di/input> "
                  "<file/csv/di/output>")
        else:
            if self.__try_call == 3:
                print("Il comando corretto e':\n"
                      "python KmerCalculator.py -n <nome-algoritmo> -input <cartella/di/input> -part "
                      "<cartella/delle/partizioni> -out <file/di/output> -k <dimensione-massima-kmer>")


