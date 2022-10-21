

class PartitionHandler:

    def create_file(self):
        """
        Metodo di creazione delle partizioni
        :return:
        """
        return NotImplementedError()

    def open_partition_path(self,mode):
        """
        :param mode
        :return:
        """
        return NotImplementedError()

    def write_skmer(self,kmer):
        """

        :param kmer:
        """
        return NotImplementedError()

    def close_file(self):
        """

        :return:
        """
        return NotImplementedError()



