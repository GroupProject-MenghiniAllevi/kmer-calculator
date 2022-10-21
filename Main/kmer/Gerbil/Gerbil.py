class Gerbil:
    """
    Questa interfaccia definisce l'algoritmo "Gerbil", che permette di contare le occorrenze dei kmer all'interno di una sequenza.
    """

    def process(self):
        """
        Questo metodo permette di eseguire l'algoritmo per calcolare i kmer e contarli.
        """
        return NotImplementedError()

    def start_first_phase_process(self):
        """
        Questo metodo permette di leggere i kmer dal file di ingresso,calcolarne i superkmer con
        i minimizer e infine inserirli in partizioni temporanei.
        """
        return NotImplementedError()

    def start_second_phase_process(self):
        """
        Questo metodo permette di leggere i superkmer dalle partizioni, contarne le occorrenze,
        inserirli in un hash table e infine scriverli nel file di output.
        """
        return NotImplementedError()

    def process_read_and_write_minimizer(self, file_fullpath, partition_file_path, filename):
        """
        Questo metodo crea le partizioni necessarie, legge i kmer da un file e infine li inserisce dentro
        una partizione nel disco.
        :param filename: il nome della molecola contenuta nel file d'ingresso.
        :param partition_file_path: percorso della cartella in cui verranno
        :param file_fullpath: il percorso completo del file.
        """
        return NotImplementedError()

    def read_from_partition_and_counting(self, partition_path, sema, molecule_name):
        """
        Questo metodo legge i kmer dentro una partizione e li inserisce dentro un map e ne calcola le occorenze
        :param sema: un meccanismo per la mutua esclusione.
        :param molecule_name: il nome della molecola di cui si sta contando i kmer
        :param partition_path: percorso dei file di partizione
        :return: un map dove come chiave viene utilizzato il kmer e il valore rappresenta il numero di occorrenze.
        """
        return NotImplementedError()
