class DirectoryHandler:

    def set_directory_path(self, path):
        """
        Questo metodo serve per impostare la cartella dove sono i presenti i file da leggere.
        :param path: il percorso della tabella.
        """

    def get_directory_path(self):
        """
        Questo metodo restituisce il percorso della cartella dei file di input.
        :return:
        """



    def get_all_files_names(self):
        """
        Questo metodo serve per sapere quali file sono presenti nella cartella.
        :return: una lista di stringhe contenente i nomi dei file.
        """


    def get_partition_file_size(self,k,filename):
        """
        Questo metodo restituisce la dimensione di una partizione.
        :param k la dimensione del singolo kmer.
        :param filename il file di cui calcolare il numero di k_mer
        :return: un  numero intero, maggiore o uguale a 0, che rappresenta la dimensione della partizione.
        """