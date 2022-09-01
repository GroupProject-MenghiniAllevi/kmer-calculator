

class DSKAlgorithm:


    def set_iteration_number(self):
        """
        Questo metodo serve per calcolare il numero di iterazioni dell'algoritmo.
        """
    def set_partition_number(self):
        """
        Questo metodo serve per calcolare il numero di partizioni che userà l'algoritmo.
        """

    def create_partition_files(self, partition_path):
        """
        Questo metodo serve per creare le partizioni al percorso stabilito.
        :param partition_path la cartella dove verranno creati i file temporanei.
        """

    def save_to_partitions(self,i):
        """
        Questo metodo implementa la prima parte dell'algoritmo DSK. Il suo obiettivo è di scrivere
        i kmer nei file temporanei.
        :param numero del'iterazione.
        """
    def process(self,partition_path, output_path):
        """
        Questo metodo implementa l'algoritmo DSK.
        :param la cartella dove le partizioni verranno salvate.
        :param il percorso del file in cui verranno salvati i k-mer con le loro occorrenze.
        """

    def initialize_hash_table(self):
        """
        Questo metodo inizializza un Hash table e lo restituisce.
        :return: l'hash table.
        """

    def write_to_output(self,lock):
        """
        Questo metodo serve per scrivere il numero di kmer e le occorrenze.
        :param lock il lock utiizzato per scrivere nel file.
        """