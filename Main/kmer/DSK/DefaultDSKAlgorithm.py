import os
import shutil
from multiprocessing import Process, Lock
from Main.kmer.DSK.DSKAlgorithm import DSKAlgorithm
from Main.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo
from Main.kmer.DSK.DefaultDSKUtils import DefaultDSKUtils
from Main.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from Main.kmer.Utils.Reader.DbNhKmerReader import DefaultDbNhReader
from Main.kmer.DSK.PartitionKmerReader import PartitionKmerReader
from Main.kmer.Utils.Reader.ExcelMoleculeReader import ExcelMoleculeReader
from Main.kmer.Utils.Writer.OutputWriter import OutputWriter


class DefaultDskAlgorithm(DSKAlgorithm):
    __k = 0
    __diskUsage = 0
    __memoryUsage = 0
    __path = ""
    __dsk_info = None
    __partition_path = ""
    __kmer_size: int
    __dh = None
    __lock = None
    __file_list = list()
    __molecules_name = dict()

    def __init__(self, k, memory_usage, disk_usage, path, partition_path):
        self.__out_path = ""
        self.__kmer_size = 0
        self.__k = k
        self.__memoryUsage = memory_usage
        self.__diskUsage = disk_usage
        self.__path = path
        self.__initialize_values()
        self.__dh = DefaultDirectoryHandler(self.__path)
        self.__file_list = self.__dh.get_all_files_names()
        self.__partition_path = partition_path
        """
        Metodo costruttore della classe

        """

    def set_iteration_number(self):
        self.__iteration_number = self.__dsk_info.iteration_number(self.__diskUsage)

    """
    Qeusto metodo imposta il numero delle iterazioni
    """

    def create_partition_files(self, partition_path, partition_number):
        p = 0
        if not os.path.exists(partition_path):
            os.mkdir(partition_path)
        while p < partition_number:
            file_name = "partition-" + str(p) + ".bin"
            fullpath = os.path.join(partition_path, file_name)
            if os.path.exists(str(fullpath)):
                file = open(fullpath, "r+")
                file.truncate()
            else:
                file = open(fullpath, "x")
            file.close()
            p = p + 1
            file = open(fullpath, "r+")
            file.close()

    """
    Questo metodo crea i file delle partizioni 
    """

    def apply_algorithm_for_file(self, filename, file_path, partition_path, lock, molecule_name):
        dsk_info = self.get_dsk_info_complete(os.path.join(self.__path, file_path))
        ith_number = dsk_info.iteration_number(self.__diskUsage)
        print("analizzando il file: " + filename)
        partition_number = dsk_info.get_partition_number(self.__memoryUsage)
        self.create_partition_files(partition_path, partition_number)
        for i in range(ith_number):
            self.save_to_partitions(i, partition_number, ith_number, file_path)
            lock.acquire()
            self.write_to_output(lock, partition_number, molecule_name, filename)
            lock.release()

    def process(self, output_path):
        self.__out_path = output_path
        lock = Lock()
        process_list = list()
        self.__molecules_name = self.detect_molecule_name_from_input()
        self.__lock = Lock()
        partition_path_list = list()
        for file in self.__file_list:
            file_without_dot = file.split(".")[0]
            partition_file_path = os.path.join(self.__partition_path, file_without_dot)
            if not os.path.exists(partition_file_path):
                os.mkdir(partition_file_path)
            partition_path_list.append(partition_file_path)
            p = Process(target=self.apply_algorithm_for_file,
                        args=(file_without_dot, file, partition_file_path, lock, self.__molecules_name[file]))
            process_list.append(p)
            p.start()
        for process in process_list:
            process.join()
        for path in partition_path_list:
            shutil.rmtree(path)

        new_out_path = os.path.dirname(self.__out_path)
        new_out_path = os.path.join(new_out_path, "new_out.csv")
        if os.path.exists(new_out_path):
            os.remove(new_out_path)

    def initialize_hash_table(self):
        ht = dict()
        return ht

    def thread_partitions_write(self, filename, j, partition_number, iteration_number):
        kmer_reader = DefaultDbNhReader()
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(os.path.join(self.__path, filename))
        k_number = kmer_reader.get_file_lenght()
        while kmer_reader.has_next(k_number):
            kmer = kmer_reader.read_next_kmer()
            dsk_utils = DefaultDSKUtils(j, kmer)
            dsk_utils.set_partition_number(partition_number)
            dsk_utils.set_iteration_number(iteration_number)
            if dsk_utils.equals_to_ith_iteration():
                dsk_utils.set_partition_index()
                path = os.path.join(self.__partition_path, filename.split(".")[0])
                path = os.path.join(path, "partition-" + str(dsk_utils.get_partition_index()) + ".bin")
                dsk_utils.write_to_partitions(path, kmer, self.__lock)
        kmer_reader.close_file()



    def save_to_partitions(self, i, partition_number, ith_number, filename):
        self.thread_partitions_write(filename, i, partition_number, ith_number)

    def write_to_output(self, lock, partition_number, molecule_name, filename):
        molecule_name = molecule_name.strip()
        for j in range(partition_number):
            hash_table = self.initialize_hash_table()
            path = os.path.join(self.__partition_path, filename)
            path = os.path.join(path, "partition-" + str(j) + ".bin")
            partition_kmer_reader = PartitionKmerReader(path, self.__k)
            size = partition_kmer_reader.get_file_lenght()
            while partition_kmer_reader.has_next(size):
                m = partition_kmer_reader.read_next_kmer()
                s = m.decode("utf-8")
                if s in hash_table:
                    hash_table[s] = hash_table[s] + 1
                else:
                    hash_table[s] = 1
            if os.path.exists(path):
                os.remove(path)
            out_writer = OutputWriter(filename=molecule_name, path=self.__out_path)
            hash_table = self.__sort_dictionary(hash_table)
            out_writer.write_to_output(hash_table)
            out_writer.close_all_files()

    def __sort_dictionary(self, ht):
        s = dict(sorted(ht.items()))
        return s

    def get_dsk_info_complete(self, filepath):
        dsk_info = DefaultDSKInfo(filepath, self.__k)
        fn = os.path.basename(os.path.normpath(filepath))
        dsk_info.getSingleKmerNumber(filepath, self.__molecules_name[fn])
        return dsk_info

    def detect_molecule_name_from_input(self):
        l = [f for f in os.listdir(self.__path) if os.path.isfile(os.path.join(self.__path, f)) and f.endswith(".xlsx")]
        excel_file_list = [v for v in l if v.endswith(".xlsx")]
        check_nH = False
        if not self.__file_list[0].find("_nH.db") == -1:
            check_nH = True
        clean_file_list = [v.replace("_nH.db", ".db") for v in self.__file_list if "_nH.db" in v]
        for excel_file in excel_file_list:
            path = os.path.join(self.__path, excel_file)
            reader = ExcelMoleculeReader(path=path)
            reader.extract_list_of_all_sheet()
            reader.extract_all_molecule_name()
            d = reader.get_molecules()
            d = self.__add_db_to_filename(d)
            for key in d:
                if key in clean_file_list:
                    s = key
                    s_index = len(s) - 3
                    if check_nH:
                        s = s[:s_index] + "_nH" + s[s_index:]
                    self.__molecules_name[s] = d[key]
        return self.__molecules_name

    def __remove_partition_file(self, filename):
        if os.path.exists(self.__partition_path + filename):
            os.remove(self.__partition_path + filename)

    def __initialize_values(self):
        self.__dsk_info = DefaultDSKInfo(self.__path, self.__k)
        self.__kmer_size = self.__dsk_info.getFullKmerNumber()

    def __add_db_to_filename(self, d):
        x = dict()
        for key in d:
            s = key + ".db"
            x[s] = d[key]
        return x
