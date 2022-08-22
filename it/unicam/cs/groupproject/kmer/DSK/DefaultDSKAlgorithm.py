import os
from pathlib import Path

from it.unicam.cs.groupproject.kmer.DSK.DSKAlgorithm import DSKAlgorithm
from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKInfo import DefaultDSKInfo


class DefaultDskAlgorithm(DSKAlgorithm):
    __k = 0

    __diskUsage = 0

    __memoryUsage = 0

    __path = ""

    __iteration_number = 0

    __partition_number = 0

    __dsk_info = None

    __partition_path = ""

    def __init__(self, k, memory_usage, disk_usage, path):
        self.__kmer_size = 0
        self.__k = k
        self.__memoryUsage = memory_usage
        self.__diskUsage = disk_usage
        self.__path = path
        self.__initialize_values()

    def set_iteration_number(self):
        self.__iteration_number = self.__dsk_info.iteration_number(self.__diskUsage)

    def set_partition_number(self):
        self.__partition_number = self.__dsk_info.get_partition_number(self.__partition_number)

    def create_partition_files(self):
        self.__partition_path = self.__get_partition_path()
        for p in range(self.__partition_number):
            file_name = "partition-" + str(p+1) + ".bin"
            file = open(file_name, "x")
            file.close()

    def process(self):
        super().process()

    def initialize_hash_table(self):
        super().initialize_hash_table()

    def write_to_output(self):
        super().write_to_output()

    def __initialize_values(self):
        self.__dsk_info = DefaultDSKInfo(self.__path, self.__k)
        self.__kmer_size = self.__dsk_info.getFullKmerNumber()


    def __get_partition_path(self):
        project_root = Path(os.path.abspath(os.path.dirname(__file__)))
        project_root = project_root.parent.absolute()
        path = os.path.join(project_root, "resource")
        path = os.path.join(path, "partitions")
        return path
