import abc


class Minimizers(metaclass=abc.ABCMeta):
    """
    Il minimizer ci permette di semplificare il calcolo di gerbil trovando un minimizer per ogni k-mer
    """

    def set_minimizer(self, minimizer):
        """
        imposta la sequenza della stringa da utilizzare come minimizer
        :param minimizer la parte della stringa da utilizzare come minimizer
        :return:
        """
        raise NotImplementedError


    def add_kmer_without_minimizer(self, kmer):
        """
        Viene presa la sequenza selezionata,aggiunta alla sequenza principale superk-mer da analizzare dividendola dal minimizer che verra
        inserito nel bin corrispondente
        :param kmer la sequenza da aggiungere
        :return:
        """
        raise NotImplementedError


    def get_super_kmer(self):
        """
        restituisce la sequenza principale dei k-mer(senza minimizer)
        :return:la sequenza principale
        """
        raise NotImplementedError