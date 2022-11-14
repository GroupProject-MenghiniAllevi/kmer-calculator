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
    
    * python KmerCalculator.py -n dsk -input D://input -part D://partizioni -out D://output/out.csv -k 3

# selezione delle features:
La selezione delle features è possibile farla tramite lo script presente nel file [FeaturesSelection.py](FeaturesSelection.py). Per avviare il programma bisogna inserire i seguenti argomenti:
-n features_selection -m <algoritmo_scelto> <percorso_file_input> <percorso_file_output>
dove:
    
    -m: Corrisponde all'algoritmo scelto per la selezione delle features. Gli algoritmi disponibili sono (da inserire senza i due punti e l'asterisco):
              
            * low_variance: Questo algoritmo eleimina le features la cui varianza è inferiore a una certa soglia. La soglia impostata è l' 80 percento.
            
            * l1_based: Questo algoritmo utilizza un modello lineare chiamato "LinearSVC" (Linear Support Vector Classification) con la penalità "l1", ovvero usando la norma (magnitudine) dei vettori generati dal modello lineare. 
    
            * chi2: Questo algoritmo attua il test del chi quadrato.

            * tree: Utilizza uno stimatore ad albero. Viene utilizzata la classe ExtraTreesClassifier che adatta un numero di alberi decisionali randomizzati su vari sottocampioni sul set di dati.

Esempio di utilizzo dello script:
    
    -python FeaturesSelection.py -n features_selection -m low_variance D://input.csv D://output/out.csv  
Il file di output, se non esiste, viene generato. Se invece il file esiste già, a questo vengono cancellati tutti i byte presenti. 


