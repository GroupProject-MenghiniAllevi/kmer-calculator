# kmer-analyzer
 Questo programma si occupa di trovare i k-mer e calcolarne le occorrenze e di selezionare le features.

# calcolo dei kmer:
Il calcolo dei kmer si può effettuare in tre modi differenti. Tutti e tre i metodi portano allo stesso risultato.
Per calcolare i kmer bisogna utilizzare il file "[KmerCalculator.py](KmerCalculator.py)". Lo script accetta i seguenti argomenti nel seguente ordine:
 -n <nome_algoritmo> -input <percorso_cartella_file_input> -part <percorso_cartella_partizioni> -out <percorso_file_output> -k <dimensione_massima_kmer>

dove:
    
    -n: corrisponde all'algoritmo scelto per calcolare i kmer. Gli algoritmi implementati sono 3: DSK, KMC3 e GERBIL.
        Per utilizzare DSK bisogna inserire "dsk". 
        Per utilizzare KMC3 bisogna inserire "kmc3". 
        Per utilizzare gerbil bisogna inserire "gerbil".

    -input: Corrisponde alla cartella dove saranno presenti i file in formato dot bracket. Più specificamente questo script è stato testato 
            con i file presenti nella sottocartella "db" della cartella "benchmark"

    -part:  Corrisponde alla cartella dove man mano vengono salvati i kmer temporaneamente. Questa cartella deve essere vuota prima di far partire lo script.
            Quando tutti i kmer vengono individuati e contate le occorrenze, verrà eliminato tutto il contenuto della cartella (ma non la cartella stessa).

    -out:   Corrisponde al file dove verranno salvati i kmer e le proprie occorrenze. 
            Se il file non esiste, questo verrà creato dallo script.

    -k:     Corrisponde alla lunghezza massima dei kmer individuati. Se ad esempio viene inserito il numero 3, 
            allora prima verranno calcolati i kmer di lunghezza uguale ad 1, poi di lunghezza uguale a 2 e infine 
            di lunghezza uguale a 3.

Esempio di utilizzo dello script:
    
    * -n dsk -input D://input -part D://partizioni -out D://output/out.csv -k 3

# selezione delle features:


