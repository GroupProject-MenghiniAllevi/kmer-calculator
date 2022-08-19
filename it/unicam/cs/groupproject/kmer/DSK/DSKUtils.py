

class DSKUtils:


    def equals_to_ith_iteration(self,kmer,ith_iteration):
        """
        Questo metodo controlla se:
            H(kmer) mod iteration_number è uguale a I.
        :param kmer: la stringa contenente il kmer.
        :param ith_iteration: numero della iterazione.
        :return: True se rispetta l'uguaglianza, False altrimenti.
        """

    def get_partition_index(self, kmer):
        """
        Questo metodo serve per calcolare a quale file temporaneo bisogna mandare il kmer.
        :param kmer: la stringa contenente il kmer
        :return: numero del file a cui mandare il kmer.
        """

    def set_iteration_number(self,iteration_number):
        """
        Questo metodo serve per impostare il numero totale di iterazioni.
        :param iteration_number: il numero totale di iterazioni.
        """

    def set_partition_number(self,partition_number):
        """
        Questo metodo serve per impostare il numero di partizioni(ovvero il numero di file temporanei).
        :param partition_number: il numero di partizioni.
        """
