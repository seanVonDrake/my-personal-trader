#!/usr/bin/python3

# SCRIPT PER LA GESTIONE DEL DATABASE DI MY PERSONAL TRADER
# 
# Questo script contiene le funzioni per la gestione del database di My Personal Trader. Può essere chiamato senza
# argomenti per stampare una breve lista dei comandi oppure con un argomento per eseguire un comando specifico,
# fra quelli riportati dalla seguente tabella:
#
# comando                                               | descrizione                           | esempio 
# ------------------------------------------------------|---------------------------------------|-----------------------------------------------
# init                                                  | crea il database                      | ./mpt-db.py init
# add symbol <symbol> <name>                            | aggiunge un simbolo al database       | ./mpt-db.py add symbol AAPL "Apple Inc."
# list symbols                                          | elenca tutti i simboli nel database   | ./mpt-db.py list symbols
# list positions                                        | elenca tutte le posizioni             | ./mpt-db.py list positions
# open position <symbol> <opened> <buy_price> <size>    | apre una nuova posizione              | ./mpt-db.py open position AAPL "2021-01-01 09:00:00" 100.00 10
# show balance                                          | mostra il bilancio                    | ./mpt-db.py show balance
# add cash <date> <amount> <description>                | aggiunge un importo al bilancio       | ./mpt-db.py add cash "2021-01-01" 1000.00 "aggiunta fondi"
# withdraw cash <date> <amount> <description>           | preleva un importo dal bilancio       | ./mpt-db.py withdraw cash "2021-01-01" 1000.00 "prelievo fondi"
#

# IMPORTAZIONE LIBRERIE
import sys
import os
import sqlite3

# VARIABILI GLOBALI
version = '0.1.1'
database = 'mpt.db'

# FUNZIONI

# connessione al database
def sqlite_connect():
    global database
    try:
        conn = sqlite3.connect( database )
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print( e )

# prelevo l'ultimo bilancio in ordine di data decrescente
def sqlite_get_last_balance( db ):
    try:

        cursor = db.cursor()
        cursor.execute( 'SELECT * FROM balance ORDER BY date DESC, id DESC LIMIT 1' )
        row = cursor.fetchone()

        if row == None:
            return 0
        else:
            return row['balance']

    except sqlite3.Error as e:
        print( e )

# inizializzazione del database
def sqlite_init_db( db ):
    try:
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS symbols
            ([symbol] TEXT PRIMARY KEY, [name] TEXT)''')
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS positions
            ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [symbol] TEXT, [opened] TEXT, [buy_price] NUMERIC, [size] NUMERIC, [closed] TEXT, [sell_price] NUMERIC, [profit] NUMERIC)''')
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS balance
            ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [date] TEXT, [amount] NUMERIC, [description] TEXT, [balance] NUMERIC)''')
    except sqlite3.Error as e:
        print( e )

# aggiunta di un simbolo al database
def sqlite_add_symbol( db, symbol, name ):
    try:
        db.cursor().execute( 'INSERT INTO symbols (symbol, name) VALUES (?, ?)', (symbol, name) )
        db.commit()
    except sqlite3.Error as e:
        print( e )

# elenco tutti i simboli del database
def sqlite_list_symbols( db ):
    try:
        cursor = db.cursor()
        cursor.execute( 'SELECT * FROM symbols' )
        for row in cursor.fetchall():
            print( row['symbol'], row['name'] )
    except sqlite3.Error as e:
        print( e )

# elenco tutte le posizioni
def sqlite_list_positions( db ):
    try:
        cursor = db.cursor()
        cursor.execute( 'SELECT * FROM positions' )
        for row in cursor.fetchall():
            print( row )
    except sqlite3.Error as e:
        print( e )

# apro una nuova posizione
def sqlite_open_position( db, symbol, opened, buy_price, size ):
    try:
        db.cursor().execute( 'INSERT INTO positions (symbol, opened, buy_price, size) VALUES (?, ?, ?, ?)', (symbol, opened, buy_price, size) )
        db.commit()
    except sqlite3.Error as e:
        print( e )

    # prelevo dal bilancio l'importo utilizzato per aprire la posizione
    amount = float(buy_price) * float(size)
    
    # aggiorno il bilancio
    sqlite_withdraw_cash( db, opened, amount, 'apertura posizione ' + symbol )

# prelevo un importo dal bilancio
def sqlite_withdraw_cash( db, date, amount, description ):

    balance = sqlite_get_last_balance( db ) - float(amount)

    try:
        db.cursor().execute( 'INSERT INTO balance (date, amount, description, balance) VALUES (?, ?, ?, ?)', (date, amount, description, balance) )
        db.commit()
    except sqlite3.Error as e:
        print( e )

# aggiungo un importo al bilancio
def sqlite_add_cash( db, date, amount, description ):

    balance = sqlite_get_last_balance( db ) + float(amount)

    try:
        db.cursor().execute( 'INSERT INTO balance (date, amount, description, balance) VALUES (?, ?, ?, ?)', (date, amount, description, balance) )
        db.commit()
    except sqlite3.Error as e:
        print( e )

# mostro il bilancio corrente
def sqlite_show_balance( db ):
    print( 'bilancio corrente: ', sqlite_get_last_balance( db ) )

# INIZIO PROGRAMMA PRINCIPALE
if __name__ == '__main__':

    # pulisco lo schermo
    os.system('clear')

    # mi connetto al database
    connection = sqlite_connect()

    # se il programma è chiamato con cinque argomenti...
    if len( sys.argv ) == 8:
        print( '7', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] )

    # se il programma è chiamato con cinque argomenti...
    elif len( sys.argv ) == 7:
        print( '6', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] )
        if sys.argv[1] == 'open' and sys.argv[2] == 'position':
            sqlite_open_position( connection, sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] )

    # se il programma è chiamato con cinque argomenti...
    elif len( sys.argv ) == 6:
        print( '5', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] )
        if sys.argv[1] == 'add' and sys.argv[2] == 'cash':
            sqlite_add_cash( connection, sys.argv[3], sys.argv[4], sys.argv[5] )
        if sys.argv[1] == 'withdraw' and sys.argv[2] == 'cash':
            sqlite_withdraw_cash( connection, sys.argv[3], sys.argv[4], sys.argv[5] )

    # se il programma è chiamato con quattro argomenti...
    elif len( sys.argv ) == 5:
        print( '4', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )
        if sys.argv[1] == 'add' and sys.argv[2] == 'symbol':
            sqlite_add_symbol( connection, sys.argv[3], sys.argv[4] )

    # se il programma è chiamato con tre argomenti...
    elif len( sys.argv ) == 4:
        print( '3', sys.argv[1], sys.argv[2], sys.argv[3] )

    # se il programma è chiamato con due argomenti...
    elif len( sys.argv ) == 3:
        print( '2', sys.argv[1], sys.argv[2] )
        if sys.argv[1] == 'list' and sys.argv[2] == 'symbols':
            sqlite_list_symbols( connection )
        elif sys.argv[1] == 'list' and sys.argv[2] == 'positions':
            sqlite_list_positions( connection )
        elif sys.argv[1] == 'show' and sys.argv[2] == 'balance':
            sqlite_show_balance( connection )

    # se il programma è chiamato con un argomento...
    elif len( sys.argv ) == 2:
        print( '1', sys.argv[1] )
        if sys.argv[1] == 'init':
            sqlite_init_db( connection )

    # se il programma è chiamato senza argomenti...
    else:
        print( 'My Personal Trader - Database Manager - v' + version )
        print( 'comandi disponibili:' )
        print( 'init                                                    crea il database e le tabelle necessarie' )
        print( 'add symbol <symbol> <name>                              aggiunge un simbolo al database' )
        print( 'list symbols                                            elenca tutti i simboli nel database' )
        print( 'list positions                                          elenca tutte le posizioni' )
        print( 'open position <symbol> <opened> <buy_price> <size>      apre una nuova posizione' )
