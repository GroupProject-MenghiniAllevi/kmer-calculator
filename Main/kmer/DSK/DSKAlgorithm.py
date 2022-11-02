
class DSKAlgorithm:


    def set_iteration_number(self):
        """
        Questo metodo serve per calcolare il numero di iterazioni dell'algoritmo.
        """
    def set_partition_number(self):
        """
        Questo metodo serve per calcolare il numero di partizioni che userà l'algoritmo.
        """

    def create_partition_files(self, partition_path, partition_number):
        """
        Questo metodo serve per creare le partizioni al percorso stabilito.
        :param partition_path la cartella dove verranno creati i file temporanei.
        :param partition_number: numero di partizioni da creare.
        """

    def save_to_partitions(self ,i, partition_number, ith_number, filename):
        """
        Questo metodo implementa la prima parte dell'algoritmo DSK. Il suo obiettivo è di scrivere
        i kmer nei file temporanei.
        :param i: numero del'iterazione.
        :param partition_number: numero totale di partizioni.
        :param ith_number: numero totale d'iterazioni.
        :param filename: il nome del file
        """
    def process(self, output_path):
        """
        Questo metodo implementa l'algoritmo DSK.
        :param output_path cartella dove le partizioni verranno salvate.
        :return il percorso del file in cui verranno salvati i k-mer con le loro occorrenze.
        """

    def initialize_hash_table(self):
        """
        Questo metodo inizializza un Hash table e lo restituisce.
        :return: l'hash table.
        """

    def write_to_output(self  ,partition_number ,molecule_name ,filename):
        """
        Questo metodo serve per scrivere il numero di kmer e le occorrenze.
        :param molecule_name: il nome della molecola che si sta scrivendo o aggiornando nel file di uscita
        :param partition_number il numero totale di partizioni.
        :param filename il nome del file d'ingresso

        """
    def get_dsk_info_complete(self, filepath):
        """
        Questo metodo restituisce un oggetto della classe dsk_info a cui è già stato calcolato la
        quantità di kmer, il numero d'iterazioni e il numero di partizioni
        :param filepath: il percorso del file d'ingresso
        :return: un oggetto di tipo dsk_info
        """

    def detect_molecule_name_from_input(self):
        """
        Questo metodo serve per determinare il nome delle molecole di cui calcolare i kmer
        :return: una lista di stringhe contenenti i nomi delle molecole presenti nel file di input.
        """

    def apply_algorithm_for_file(self, filename, file_path, partition_path, molecule_name):
        """
        Questo metodo applica l'algoritmo al file passato come ingresso.
        :param file_path: il nome completo del file
        :param molecule_name: il nome della molecola
        :param filename: il nome del file su cui applicare l'algoritmo dsk.
        :param partition_path: il percorso dove creare le partizioni.
        """
