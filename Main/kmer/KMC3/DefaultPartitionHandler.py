import os.path

from Main.kmer.KMC3.PartitionHandler import PartitionHandler
from Main.kmer.Utils.minimizer.DefaultMinimizerHandler import DefaultMinimizerHandler
from Main.kmer.Utils.Writer.DefaultSKmerWriter import DefaultSKmerWriter


class DefaultPartitionHandler(PartitionHandler):
    __path = ""
    __file = None
    __ith_minimizer = -1
    __super_kmer_size = -1
    __minimizer_handler = None
    __skmer_writer = None
    __minimizer = ""
    __kmer_list = list()
    __skmer_reader = None

    def __init__(self, minimizer, path, super_kmer_size, k,m):
        """
        Metodo di creazione della classe
        :param minimizer: il minimizer che prenderà il nome del file
        :param path:
        :param super_kmer_size:
        :param k:
        """
        filename = minimizer + ".bin"
        self.__path = os.path.join(path, filename)
        self.__super_kmer_size = super_kmer_size
        self.__minimizer = minimizer
        self.__minimizer_handler = DefaultMinimizerHandler(k=k, m=len(minimizer))
        self.__skmer_writer = DefaultSKmerWriter(k=k, m=len(minimizer))
        self.__ith_minimizer = 0

    def create_file(self):
        self.__check_path_error()
        with open(self.__path, "x") as file:
            file.close()

    def open_partition_path(self, mode):
        self.__check_path_error()
        if not os.path.exists(self.__path):
            raise Exception("la partizione non è stata creata.")
        if mode == "r":
            m = "rb"
        else:
            m = "wb"
        try:
            self.__file = open(self.__path, m)
        except:
            raise Exception("errore nell'apertura del file.")

    def write_skmer(self, kmer):
        if self.__ith_minimizer == 0:
            self.__minimizer = self.__minimizer_handler.get_minimizers_from_kmer(kmer)
            self.__ith_minimizer += 1
            self.__kmer_list.append(kmer)
        elif self.__ith_minimizer == self.__super_kmer_size - 1:
            self.__kmer_list.append(kmer)
            self.__minimizer_handler.find_super_kmer_and_write(self.__kmer_list, self.__minimizer, self.__path)
            self.__kmer_list.clear()
            self.__ith_minimizer = 0
        else:
            self.__ith_minimizer += 1
            self.__kmer_list.append(kmer)

    def close_file(self):
        if not self.__file.closed:
            self.__file.close()

    def __check_path_error(self):
        if self.__path == "":
            raise Exception("non è stato impostato il percorso del file usato come partizione.")
