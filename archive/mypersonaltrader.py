# questo programma viene chiamato ogni tot (ad esempio ogni ora) e gestisce le posizioni su una
# lista di simboli dati; utilizza un sistema molto semplice per decidere se aprire o chiudere le
# posizioni

# IMPORTAZIONI
# il pacchetto sys ci consente di gestire gli argomenti da linea di comando, mentre il pacchetto os ci serve per intervenire sui file
# i pacchetti datetime e dateutil.parser ci servono per maneggare le date
# il pacchetto sqlite3 ci serve per gestire il database sqlite dove vengono salvati i dati di lavoro dell'applicazione
# i pacchetti yfinance e yfinance_cache servono a raccogliere i dati da Yahoo Finance (yfinance_cache ha più o meno le stesse funzionalità di yfinance ma dovrebbe utilizzare una cache locale in modo da ridurre i tempi di download)
# il pacchetto pandas ci serve per gestire i dataset
import sys
import os
import datetime
import dateutil.parser
import sqlite3
import yfinance
import yfinance_cache
import pandas

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
        ([symbol] TEXT PRIMARY KEY, [position] TEXT, [opened] TEXT, [price] NUMERIC)
        ''')

# funzione per l'aggiunta di un simbolo al database
def sqlite_add_symbol( db, symbol ):
    c = db.cursor()
    sql = ''' INSERT INTO symbols VALUES( ?, ?, ?, ? ) '''
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

# funzione che decide cosa fare con un titolo
def strategy_3ma( data, today ):

    yesterday = today - datetime.timedelta( days = 1 )

    interval = pandas.DataFrame( data )

    close = interval[ 'Close' ]

    sma10 = close.rolling( window = 10 ).mean()
    sma20 = close.rolling( window = 20 ).mean()
    sma30 = close.rolling( window = 30 ).mean()

    price = close[ yesterday.strftime( '%Y-%m-%d' ) ]
    sma10v = sma10[ yesterday.strftime( '%Y-%m-%d' ) ]
    sma20v = sma20[ yesterday.strftime( '%Y-%m-%d' ) ]
    sma30v = sma30[ yesterday.strftime( '%Y-%m-%d' ) ]

    print( yesterday, '(ieri) prezzo di chiusura ->', close[ yesterday.strftime( '%Y-%m-%d' ) ], 'SMA 10 ->', sma10v, 'SMA 20 ->', sma20v, 'SMA 30 ->', sma30v )

    if price > sma30v:
        return 'LONG'
    elif price <= sma30v:
        return 'SHORT'

# funzione che prende il prezzo corrente di un simbolo
# NOTA questa funzione è in sviluppo, utilizzare solo per i test!
def get_price( symbol, decision, date ):

    # se la data è storica, prendo il valore storico
    if date < datetime.date.today():
        print( 'è stata richiesta una data storica' )
        ticker = yfinance_cache.Ticker( symbol )
        end = date + datetime.timedelta( days = 1 )
        values = ticker.history( interval = '1d', start = date, end = end )
        interval = pandas.DataFrame( values )
        close = interval[ 'Close' ]
        price = close[ date.strftime( '%Y-%m-%d' ) ]

    else:
        stock = yfinance.Ticker( symbol )
        price = stock.info['regularMarketPrice']

    print( 'il prezzo corrente per', symbol, 'al', date, 'è', price )

    return price

# funzione che apre una posizione
def open_position( db, symbol, decision, today ):
    price = get_price( symbol, decision, today )
    print( 'apro', decision, 'per', symbol, 'a', price, 'dollari' )
    # TODO scrivo nel database la decisione, la data e il prezzo

# funzione che chiude una posizione
def close_position( db, symbol, decision, today ):
    price = get_price( symbol, decision, today )
    print( 'chiudo', decision, 'per', symbol, 'a', price, 'dollari' )
    # TODO leggo dal database la decisione, la data e il prezzo
    # TODO scrivo il file di report dell'operazione
    # TODO svuoto nel database la decisione, la data e il prezzo

# INIZIO PROGRAMMA PRINCIPALE
# la prima sezione del programma gestisce gli argomenti da linea di comando dati dall'utente per gestire il database (aggiunta, rimozione e visualizzazione dei simboli)
# mentre la seconda parte fa i trade veri e propri
if __name__ == '__main__':

    # apro il database
    db = sqlite_connect()

    # se il programma è chiamato con tre argomenti...
    if len( sys.argv ) == 3:
        if sys.argv[1] == 'reset' and sys.argv[2] == 'database':
            print( 'azzero il database' )
            os.remove( 'mypersonaltrader.db' )
        if sys.argv[1] == 'show' and sys.argv[2] == 'symbol':
            data = sqlite_get_symbols( db )
            for row in data:
                print( row )

    # se il programma è chiamato con due argomenti...
    elif len( sys.argv ) == 4:
        if sys.argv[1] == 'add' and sys.argv[2] == 'symbol':
            print( 'aggiungo il simbolo', sys.argv[3] )
            sqlite_add_symbol( db, sys.argv[3] )

        elif sys.argv[1] == 'remove' and sys.argv[2] == 'symbol':
            print( 'rimuovo il simbolo', sys.argv[3] )
            sqlite_remove_symbol( db, sys.argv[3] )

    # funzionamento base del programma (un argomento o nessun argomento)
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
                today = datetime.datetime.strptime( sys.argv[1], '%Y-%m-%d' ).date()
            else:
                today = datetime.date.today()

        # leggo la lista dei simboli
        data = sqlite_get_symbols( db )

        # elaborazione di ogni simbolo
        for symbol in data:

            # output
            print( 'lavoro sul simbolo:', symbol['symbol'], 'per la data', today )

            # data di inizio periodo storico dati
            start = today - datetime.timedelta( days = 365 )

            # per ogni simbolo, scarico il dataset aggiornato
            ticker = yfinance_cache.Ticker( symbol['symbol'] )
            values = ticker.history( interval = '1d', start = start, end = today )

            # chiamo la funzione di valtuazione per sapere se il segnale di oggi è LONG o SHORT
            decision = strategy_3ma( values, today )

            # output
            print( 'la decisione è di andare', decision )

            # se non ho una posizione aperta
            if symbol['position'] == None:
                print( 'non ho una posizione aperta per', symbol['symbol'] )

                # se non ho una posizione aperta e il segnale è LONG apro LONG
                if decision == 'LONG':
                    print( 'apro una posizione', decision, 'per', symbol['symbol'] )
                    open_position( db, symbol['symbol'], decision, today )

                # se non ho una posizione aperta e il segnale è SHORT apro SHORT
                elif decision == 'SHORT':
                    print( 'apro una posizione', decision, 'per', symbol['symbol'] )
                    open_position( db, symbol['symbol'], decision, today )

                # se c'è un segnale di indecisione
                else:
                    print( 'ho un segnale di indecizione e non apro una posizione per', symbol['symbol'] )

            # se ho una posizione aperta LONG
            elif symbol['position'] == 'LONG':

                # se ho una posizione aperta LONG e il segnale è LONG non faccio nulla
                if decision == 'LONG':
                    print( 'mantengo la posizione', decision, 'per', symbol['symbol'] )

                # se ho una posizione aperta LONG e il segnale è SHORT chiudo la posizione LONG e apro una posizione SHORT
                elif decision == 'SHORT':
                    print( 'chiudo la posizione', symbol['position'], 'per', symbol['symbol'] )
                    close_position( db, symbol['symbol'], decision, today )
                    print( 'apro una posizione', decision, 'per', symbol['symbol'] )
                    open_position( db, symbol['symbol'], decision, today )

                # se c'è un segnale di indecisione
                else:
                    print( 'ho un segnale di indecizione e non modifico la posizione', symbol['position'], 'per', symbol['symbol'] )

            # se ho una posizione aperta SHORT
            elif symbol['position'] == 'SHORT':

                # se ho una posizione aperta SHORT e il segnale è LONG chiudo la posizione SHORT e apro una posizione LONG
                if decision == 'LONG':
                    print( 'chiudo la posizione', symbol['position'], 'per', symbol['symbol'] )
                    close_position( db, symbol['symbol'], decision, today )
                    print( 'apro una posizione', decision, 'per', symbol['symbol'] )
                    open_position( db, symbol['symbol'], decision, today )

                # se ho una posizione aperta SHORT e il segnale è SHORT non faccio nulla
                elif decision == 'SHORT':
                    print( 'mantengo la posizione', decision, 'per', symbol['symbol'] )

                # se c'è un segnale di indecisione
                else:
                    print( 'ho un segnale di indecizione e non modifico la posizione', symbol['position'], 'per', symbol['symbol'] )


