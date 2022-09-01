import os
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

    __iteration_number = 0

    __partition_number = 0

    __dsk_info = None

    __partition_path = ""
    __kmer_size: int

    __lock = None

    def __init__(self, k, memory_usage, disk_usage, path):
        self.__out_path = ""
        self.__kmer_size = 0
        self.__k = k
        self.__memoryUsage = memory_usage
        self.__diskUsage = disk_usage
        self.__path = path
        self.__initialize_values()
        """
        Metodo costruttore della classe

        """

    def set_iteration_number(self):
        self.__iteration_number = self.__dsk_info.iteration_number(self.__diskUsage)

    """
    Qeusto metodo imposta il numero delle iterazioni
    """

    def set_partition_number(self):
        self.__partition_number = self.__dsk_info.get_partition_number(self.__memoryUsage)

    """
    Questo metodo imposta il numero delle partizioni
    """

    def create_partition_files(self, partition_path):
        self.__partition_path = partition_path
        p = 0
        while p < self.__partition_number:
            file_name = "partition-" + str(p) + ".bin"
            fullpath = os.path.join(self.__partition_path, file_name)
            if os.path.exists(str(fullpath)):
                file = open(fullpath, "r+")
                file.truncate()
            else:
                file = open(fullpath, "x")

            file.close()
            p = p + 1

    """
    Questo metodo crea i file delle partizioni 
    """

    def process(self, partition_path, output_path):
        self.__out_path = output_path
        self.__partition_path = partition_path
        process_list = list()
        self.__lock = Lock()
        for i in range(self.__iteration_number):
            self.create_partition_files(partition_path)
            self.save_to_partitions(i)
            p = Process(target=self.write_to_output, args=(self.__lock,))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()
        for j in range(self.__partition_number):
            self.__remove_partition_file("/partition-" + str(j) + ".bin")

    def initialize_hash_table(self):
        ht = dict()
        return ht

    def thread_partitions_write(self, filename, j, k_number):
        kmer_reader = DefaultKmerReader()
        kmer_reader.set_kmer_lenght(self.__k)
        kmer_reader.set_path(self.__path + "/" + filename)
        while kmer_reader.has_next(k_number):
            kmer = kmer_reader.read_next_kmer()
            dsk_utils = DefaultDSKUtils(j, kmer)
            dsk_utils.set_partition_number(self.__partition_number)
            dsk_utils.set_iteration_number(self.__iteration_number)
            if dsk_utils.equals_to_ith_iteration():
                dsk_utils.set_partition_index()
                fullpath = self.__partition_path + "/partition-" + dsk_utils.get_partition_index() + ".bin"
                dsk_utils.write_to_partitions(fullpath, kmer, self.__lock)

    def save_to_partitions(self, i):
        list_of_file = self.__list_of_file()
        process_list = list()
        for file in list_of_file:
            dh = DefaultDirectoryHandler(self.__path)
            size = dh.get_file_size(file)
            p = Process(target=self.thread_partitions_write,
                        args=(file, i, self.__dsk_info.getSingleKmerNumber(size)))
            p.start()
            process_list.append(p)
        for process in process_list:
            process.join()

    def write_to_output(self, lock):
        out_writer = OutputWriter()
        for j in range(self.__partition_number):
            hash_table = self.initialize_hash_table()
            partition_kmer_reader = PartitionKmerReader(self.__partition_path + "/partition-" + str(j) + ".bin",
                                                        self.__k)
            size = partition_kmer_reader.get_file_lenght()
            if partition_kmer_reader.get_file_lenght() > 0:
                while partition_kmer_reader.has_next(size):
                    m = partition_kmer_reader.read_next_kmer()
                    s = m.decode("utf-8")
                    if s in hash_table:
                        hash_table[s] = hash_table[s] + 1
                    else:
                        hash_table[s] = 1
                lock.acquire()
                out_writer.write_to_output(self.__out_path, hash_table, j)
                lock.release()
    def __remove_partition_file(self, filename):

        if os.path.exists(self.__partition_path + filename):
            os.remove(self.__partition_path + filename)

    def __initialize_values(self):
        self.__dsk_info = DefaultDSKInfo(self.__path, self.__k)
        self.__kmer_size = self.__dsk_info.getFullKmerNumber()

    def __list_of_file(self):
        dh = DefaultDirectoryHandler(self.__path)
        return dh.get_all_files_names()
