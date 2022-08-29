

class KmerReader:
    pass


    def read_next_kmer(self):
        """
        Questo metodo permette di leggere il prossimo kmer nel file
        :return: una stringa contenente il kmer
        """


    def set_kmer_lenght(self,k):
        """
        Questo metodo imposta la lunghezza del kmer da leggere
        :param k: un intero che rappresenta la lunghezza del kmer.
        """


    def set_path(self, path):
        """
        Questo metodo imposta il percorso del file da leggere e apre il file, facendo in modo che quando il
        file viene letto, si legga solo le sequenze esatte.
        :param path: una stringa che rappresenta il percorso del file.
        """


    def has_next(self, kmer_size):
        """
        Questo metodo controlla se la sequenza letta fino ad ora non sia finita.
        :param kmer_size il numero di kmer da leggere.
        :return: True se non è finita, False altrimenti.
        """

    def get_file_lenght(self):
        """
        Questo metodo restituisce il numero di kmer presenti nel file.
        :return: la lunghezza del file.
        """

