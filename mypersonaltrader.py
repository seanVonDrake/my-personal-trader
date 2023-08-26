# questo programma viene chiamato ogni tot (ad esempio ogni ora) e gestisce le posizioni su una
# lista di simboli dati; utilizza un sistema molto semplice per decidere se aprire o chiudere le
# posizioni

# IMPORTAZIONI
# il pacchetto sys ci consente di gestire gli argomenti da linea di comando, mentre il pacchetto os ci serve per intervenire sui file
# il pacchetto dateutil.parser ci serve per maneggare le date
# il pacchetto sqlite3 ci serve per gestire il database sqlite dove vengono salvati i dati di lavoro dell'applicazione
import sys
import os
import dateutil.parser
import sqlite3

# funzione per la connessione al database
def sqlite_connect():
    db = None
    try:
        db = sqlite3.connect( 'mypersonaltrader.db' )
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='symbols' ''')
        if c.fetchone()[0]==0 :
            sqlite_init_db( db )
        return db
    except sqlite3.Error as e:
        print( e )

# funzione per l'inizializzazione del database
def sqlite_init_db( db ):
    c = db.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS symbols
        ([symbol] TEXT PRIMARY KEY, [position] TEXT)
        ''')

# funzione per l'aggiunta di un simbolo al database
def sqlite_add_symbol( db, symbol ):
    c = db.cursor()
    sql = ''' INSERT INTO symbols VALUES( ?, ? ) '''
    c.execute( sql, ( symbol, None ) )
    db.commit()

# funzione per la rimozione di un simbolo dal database
def sqlite_remove_symbol( db, symbol ):
    c = db.cursor()
    sql = ''' DELETE FROM symbols WHERE symbol = ? '''
    c.execute( sql, ( symbol, ) )
    db.commit()

# funzione per leggere i simboli presenti nel database
def sqlite_get_symbols( db ):
    c = db.cursor()
    sql = ''' SELECT * FROM symbols '''
    c.execute( sql )
    return c.fetchall()

# funzione che serve per capire se una stringa contiene una data
def is_date( string, fuzzy = False ):
    try: 
        dateutil.parser.parse( string, fuzzy = fuzzy )
        return True
    except ValueError:
        return False

# INIZIO PROGRAMMA PRINCIPALE
# la prima sezione del programma gestisce gli argomenti da linea di comando dati dall'utente per gestire il database (aggiunta, rimozione e visualizzazione dei simboli)
# mentre la seconda parte fa i trade veri e propri

if __name__ == '__main__':

    # apro il database
    db = sqlite_connect()

    # se il programma è chiamato con degli argomenti...
    if len( sys.argv ) == 3:
        if sys.argv[1] == 'reset' and sys.argv[2] == 'database':
            print( 'azzero il database' )
            os.remove( 'mypersonaltrader.db' )
        if sys.argv[1] == 'show' and sys.argv[2] == 'symbol':
            data = sqlite_get_symbols( db )
            for row in data:
                print( row )

    elif len( sys.argv ) == 4:
        if sys.argv[1] == 'add' and sys.argv[2] == 'symbol':
            print( 'aggiungo il simbolo', sys.argv[3] )
            sqlite_add_symbol( db, sys.argv[3] )

        elif sys.argv[1] == 'remove' and sys.argv[2] == 'symbol':
            print( 'rimuovo il simbolo', sys.argv[3] )
            sqlite_remove_symbol( db, sys.argv[3] )

    else:

        # gestione linea di comando a singolo argomento
        if len( sys.argv ) == 2:
            if sys.argv[1] == 'help':
                print( 'utilizzare:' )
                print( 'reset database -> azzera il database' )
                print( 'add symbol <symbol> -> aggiunge il simbolo al database' )
                print( 'remove symbol <symbol> -> rimuove il simbolo dal database' )
                print( 'show symbol -> elenca i simboli presenti nel database' )
                print( '<data> -> per lavorare su una data specifica anziché oggi' )
            elif is_date( sys.argv[1] ):
                print( 'lavoro sulla data custom:', sys.argv[1] )

        # leggo la lista dei simboli
        data = sqlite_get_symbols( db )

        # elaborazione di ogni simbolo
        for symbol in data:
            print( 'lavoro sul simbolo:', symbol['symbol'] )

            # per ogni simbolo, scarico il dataset aggiornato
            # NOTA questa cosa si può forse rendere più efficiente salvando nel database le porzioni storiche
            # del dataset e scaricando solo gli ultimi due giorni (ieri e oggi)

            # chiamo la funzione di valtuazione per sapere se il segnale di oggi è LONG o SHORT

            # leggo se ho una posizione aperta nel database

            # se non ho una posizione aperta e il segnale è LONG apro LONG

            # se ho una posizione aperta LONG e il segnale è LONG non faccio nulla

            # se ho una posizione apert SHORT e il segnale è LONG chiudo la posizione SHORT e apro una posizione LONG

            # se non ho una posizione aperta e il segnale è SHORT apro SHORT

            # se ho una posizione aperta LONG e il segnale è SHORT chiudo la posizione LONG e apro una posizione SHORT

            # se ho una posizione aperta SHORT e il segnale è SHORT non faccio nulla


