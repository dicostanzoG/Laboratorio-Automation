# Laboratorio-Automation

Implementazione dell'algoritmo Probabilistic Roadmap e confronto della costruzione del grafo con k-neighbors o con ε-neighborhood.

Gli __ostacoli__ sono creati nella funzione _generate_obstacles()_ ed è verificato che non si sovrappongono con la funzione _obs_collision()_, utilizzando le bounding box.

I punti __start__ e __goal__ sono creati randomicamente nella funzione _random_point()_ verificando che non ci sia intersezione con gli ostacoli.

La funzione _create_graph()_ inizializza il grafo aggiungendo i punti start e goal come nodi.

La funzione _prm()_ implementa l'algoritmo Probabilistic Roadmap e mostra il plot del grafo creato, l'algoritmo si ferma quando si crea un cammino tra start e goal e si raggiunge il numero di nodi desiderato (per avere un grafo abbastanza denso). 

L'insieme dei nodi vicini del punto randomico è creato o trovando i k nodi più vicini, implementando la funzione _knn()_, o trovando tutti quelli a una distanza inferiore di ε, con la funzione _eps_n()_.

La funzione _free_path()_ verifica se la retta (arco) che collega due nodi interseca un ostacolo.

I punti start e goal sono rappresentati nel plot con il colore rosso mentre i nodi che fanno parte di uno dei cammini minimi sono blu e gli archi che collegano questi nodi sono rossi.

Per effettuare il confronto è stato calcolato il tempo impiegato dalla funzione _prm()_ sia per il caso con k-neighbors che con ε-neighborhood, con la stessa configurazione iniziale (start, goal e ostacoli) effettuando una media su più iterazioni. Inoltre sono stati calcolati in entrambi i casi il numero di componenti connesse e il numero di nodi creati.

Si è potuto stabilire che l'algoritmo di PRM con _ε-neighborhood_, scegliendo un raggio ε piccolo, impiega più tempo generando un numero elevato di nodi rispetto alla versione con _k-neighbors_.

Nel video si può vedere un esempio dell'algoritmo implementato.
