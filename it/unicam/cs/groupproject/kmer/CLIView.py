from it.unicam.cs.groupproject.kmer.DSK.DefaultDSKAlgorithm import DefaultDskAlgorithm


class CLIView():
    __argc = 0
    __argv = []

    def __init__(self, argc, argv):
        self.__argv = argv
        self.__argc = argc

    def check_if_is_help(self):
        if self.__argc == 2 and self.__argv[1] == '-h':
            print("se l'argomento è obbligatorio allora è seguito da due parentesi quadre.")
            print("per selezionare l'algoritmo dsk i primi due argomenti devono essere: -n dsk")
            print("argomenti dell'algoritmo DSK:\n"
                  "-input []       il percorso della cartella dei file di input.    \n\n"
                  "-part []        il percorso della cartella dei file di partizione\n"
                  "                usati come appoggio temporaneo per il calcolo dei\n"
                  "                kmer.\n\n"
                  "-out []         il percorso della cartella del file di output.   \n\n"
                  "-k              dimensione del kmer")

    def check_if_is_DSK(self):
        if self.__argv[1] == "-n" and self.__argv[2] == "dsk":
            input_path = self.__argv[4]
            part = self.__argv[6]
            output = self.__argv[8]
            k = int(self.__argv[10])
            dsk = DefaultDskAlgorithm(k, 81920, 81920, input_path)
            dsk.set_iteration_number()
            dsk.set_partition_number()
            dsk.process(part, output)
