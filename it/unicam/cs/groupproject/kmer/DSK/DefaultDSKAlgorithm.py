import os
import shutil
from multiprocessing import Process, Lock
from it.unicam.cs.groupproject.kmer.DSK.DSKAlgorithm import DSKAlgorithm
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKUtils import DefaultDSKUtils
from it.unicam.cs.groupproject.kmer.Utils.DefaultDirectoryHandler import DefaultDirectoryHandler
from it.unicam.cs.groupproject.kmer.Utils.DefaultKmerReader import DefaultKmerReader
from it.unicam.cs.groupproject.kmer.DSK.PartitionKmerReader import PartitionKmerReader
from it.unicam.cs.groupproject.kmer.Utils.OutputWriter import OutputWriter


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
        partition_number = dsk_info.get_partition_number(self.__memoryUsage)
        self.create_partition_files(partition_path, partition_number)
        for i in range(ith_number):
            self.save_to_partitions(i, partition_number, ith_number, file_path)
            lock.acquire()
            self.write_to_output(lock, partition_number, molecule_name, filename)
            lock.release()

    def process(self, partition_path, output_path):
        self.__out_path = output_path
        self.__partition_path = partition_path
        lock = Lock()
        with open(self.__out_path, "wb+") as ff:
            ff.truncate()
            ff.close()

        self.__file_list = self.__dh.get_all_files_names()
        process_list = list()
        self.detect_molecule_name_from_input()
        self.__lock = Lock()
        partition_path_list = list()
        for file in self.__file_list:
            file_without_dot = file.split(".")[0]
            partition_file_path = os.path.join(partition_path, file_without_dot)
            if not os.path.exists(partition_file_path):
                os.mkdir(partition_file_path)
            partition_path_list.append(partition_file_path)
            # p = Process(target=self.apply_algorithm_for_file, args=(file_without_dot,file, partition_file_path, lock,self.__molecules_name[file]))
            # process_list.append(p)
            # p.start()
            self.apply_algorithm_for_file(file_without_dot, file, partition_file_path, lock,
                                          self.__molecules_name[file])
        for process in process_list:
            pass
        for path in partition_path_list:
                shutil.rmtree(path)
            # process.join()

        new_out_path = os.path.dirname(self.__out_path)
        new_out_path = os.path.join(new_out_path,"new_out.csv")
        if os.path.exists(new_out_path):
            os.remove(new_out_path)

    def initialize_hash_table(self):
        ht = dict()
        return ht

    def thread_partitions_write(self, filename, j, partition_number, iteration_number):
        kmer_reader = DefaultKmerReader()
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(os.path.join(self.__path, filename))
        k_number = kmer_reader.get_file_lenght()
        # print("leggendo il file di input... ", filename, " k_number", k_number)
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
        # print("iniziando a salvare nelle partizioni il file ", filename)
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
                #print(filename, m)
                s = m.decode("utf-8")
                if s in hash_table:
                    hash_table[s] = hash_table[s] + 1
                else:
                    hash_table[s] = 1
            if os.path.exists(path):
                os.remove(path)
            out_writer = OutputWriter(filename=molecule_name, path=self.__out_path)
            out_writer.write_to_output(hash_table)
            hash_table = self.initialize_hash_table()
            out_writer.close_all_files()

    def get_dsk_info_complete(self, filepath):
        dsk_info = DefaultDSKInfo(filepath, self.__k)
        dsk_info.getSingleKmerNumber(filepath)
        return dsk_info

    def detect_molecule_name_from_input(self):
        for file in self.__file_list:
            reader = DefaultKmerReader()
            path = os.path.join(self.__path, file)
            reader.set_path(path)
            self.__molecules_name[file] = reader.get_file_name()
            reader.close_file()

    def __remove_partition_file(self, filename):
        if os.path.exists(self.__partition_path + filename):
            os.remove(self.__partition_path + filename)

    def __initialize_values(self):
        self.__dsk_info = DefaultDSKInfo(self.__path, self.__k)
        self.__kmer_size = self.__dsk_info.getFullKmerNumber()

    def __list_of_file(self):
        dh = DefaultDirectoryHandler(self.__path)
        return dh.get_all_files_names()
