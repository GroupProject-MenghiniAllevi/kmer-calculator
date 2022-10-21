class KMC3:

    def write_kmer_to_partition(self, partition_sub_path, input_file_path):
        """
        Questo metodo permette di leggere i kmer presenti nel file d'ingresso, crea i super-kmer e li scrive nelle partizioni.
        :param partition_sub_path: percorso della cartella dove verranno salvate le partizioni.
        :param input_file_path: percorso del file d'ingresso.
        """
        return NotImplementedError()

    def read_skmer_and_print_to_output(self, filepart_path):
        """
        Questo metodo stampa il superKmer
        :param filepart_path:
        :return:
        """

    def process(self):
        """
        Questo metodo si occupa di leggere e contare i kmer e infine d'inserirli nel file di uscita.
        """
        return NotImplementedError()

    def extract_file_list(self):
        """
        Questo metodo restituisce la lista di file d'ingresso presenti nella cartella d'ingresso.
        :return: una lista di stringhe che rappresentano i nomi dei file d'ingresso.
        """
        return NotImplementedError()

    def create_partitions(self, partitions_path, file_list):
        """
        Questo metodo crea le partizioni
        :return:
        """
        return NotImplementedError()

    def extract_molecule_name(self):
        """
        Questo metodo estrae il nome della molecola
        :return:
        """
        return NotImplementedError()
