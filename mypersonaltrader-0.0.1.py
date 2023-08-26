# questo programma viene chiamato ogni tot (ad esempio ogni ora) e gestisce le posizioni su una
# lista di simboli dati; utilizza un sistema molto semplice per decidere se aprire o chiudere le
# posizioni

# lavoro con la data di oggi OPPURE con una data arbitraria (per fare i test)
# NOTA per testare questa applicazione basta chiamarla N volte specificando ogni volta
# una data incrementata di un giorno, in questo modo si vedranno le posizioni che si
# evolvono nel database

# apro il database

# leggo la lista dei simboli

# leggo la lista delle posizioni aperte

# per ogni simbolo, scarico il dataset aggiornato
# NOTA questa cosa si può forse rendere più efficiente salvando nel database le porzioni storiche
# del dataset e scaricando solo gli ultimi due giorni (ieri e oggi)

# ciclo per ogni simbolo...

    # chiamo la funzione di valtuazione per sapere se il segnale di oggi è LONG o SHORT

    # leggo se ho una posizione aperta nel database

    # se non ho una posizione aperta e il segnale è LONG apro LONG

    # se ho una posizione aperta LONG e il segnale è LONG non faccio nulla

    # se ho una posizione apert SHORT e il segnale è LONG chiudo la posizione SHORT e apro una posizione LONG

    # se non ho una posizione aperta e il segnale è SHORT apro SHORT

    # se ho una posizione aperta LONG e il segnale è SHORT chiudo la posizione LONG e apro una posizione SHORT

    # se ho una posizione aperta SHORT e il segnale è SHORT non faccio nulla


