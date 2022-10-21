class DSKUtils:

    def equals_to_ith_iteration(self):
        """
        Questo metodo controlla se:
            H(kmer) mod iteration_number è uguale a I.
        :return: True se rispetta l'uguaglianza, False altrimenti.
        """

    def set_partition_index(self):
        """
        Questo metodo serve per calcolare e memorizzare a quale file temporaneo bisogna mandare il kmer.
        """

    def set_iteration_number(self, iteration_number):
        """
        Questo metodo serve per impostare il numero totale di iterazioni.
        :param iteration_number: il numero totale di iterazioni.
        """

    def set_partition_number(self, partition_number):
        """
        Questo metodo serve per impostare il numero di partizioni(ovvero il numero di file temporanei).
        :param partition_number: il numero di partizioni.
        """

    def get_hash(self):
        """
        Questa funzione restituisce un hash a 64 bit intero del kmer.
        :return: l'hash del kmer.
        """

    def write_to_partitions(self, path, kmer, lock):
        """
        :param path:
        :param kmer:
        :return:
        """

    def get_partition_index(self):
        """
        Questa funzione restituisce l'indice del file termporaneo in cui scrivere il kmer.
        :return: un intero che rappresenta l'indice
        """


