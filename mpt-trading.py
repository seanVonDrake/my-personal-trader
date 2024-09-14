#!/usr/bin/python3

# SCRIPT PER LA GESTIONE DEI TRADING DI MY PERSONAL TRADER
#
# Questo script si occupa di fare i trading veri e propri. Può essere chiamato senza argomenti per stampare una breve
# lista dei comandi oppure con un argomento per eseguire un comando specifico, fra quelli riportati dalla seguente tabella:
#
# comando                                               | descrizione                                                                                           | esempio
# ------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------
# advice symbol <symbol>                                | fornisce un consiglio di trading                                                                      | ./mpt-trading.py advice AAPL
# advice symbol <symbol> <date>                         | fornisce un consiglio di trading a una data specifica (per i backtest)                                | ./mpt-trading.py advice AAPL 2024-03-18 
# advice position <id>                                  | fornisce un consiglio di trading                                                                      | ./mpt-trading.py advice position 1
# advice position <id> <date>                           | fornisce un consiglio di trading a una data specifica (per i backtest)                                | ./mpt-trading.py advice position 1 2024-03-18
# get price <symbol>                                    | fornisce il prezzo attuale di un simbolo                                                              | ./mpt-trading.py get price AAPL
# get price <symbol> <date>                             | fornisce il prezzo di un simbolo a una data specifica (per i backtest)                                | ./mpt-trading.py get price AAPL 2024-03-18
# get sma <symbol> <period>                             | fornisce la media mobile semplice di un simbolo per un periodo specifico                              | ./mpt-trading.py get sma AAPL 50
# get sma <symbol> <period> <date>                      | fornisce la media mobile semplice di un simbolo per un periodo specifico a partire da una certa data  | ./mpt-trading.py get ema AAPL 50 2024-03-18                             
#

# IMPORTAZIONE LIBRERIE
import sys
import os
import sqlite3
import datetime
import yfinance_cache
import pandas

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

# consiglio di trading per un simbolo
def trading_advice_symbol( db, symbol, date = None ):
    if date is None:
        date = datetime.datetime.today()
    else:
        date = datetime.datetime.strptime( date, '%Y-%m-%d' )
    # start = date - datetime.timedelta( days = 5 )
    start = date
    votes = []
    days = 1
    while len( votes ) < 5:
        evdate = start - datetime.timedelta( days = days )
        print( 'Evaluating', symbol, 'on', evdate.strftime( '%Y-%m-%d' ) )
        details = get_price_details( symbol, evdate.strftime( '%Y-%m-%d' ) )
        days += 1
        if details != None:
            votes.append( 1 )
            print( 'open on', details['Open'], 'close on', details['Close'] )
    print( 'My trading advice for symbol', symbol, 'on', date.strftime( '%Y-%m-%d' ), 'is' )

# consiglio di trading per una posizione
def trading_advice_position( db, id ):
    try:
        cursor = db.cursor()
        cursor.execute( 'SELECT * FROM positions WHERE id = ?', (id,) )
        row = cursor.fetchone()
        print( 'Trading advice for position', id, row['symbol'] )
    except sqlite3.Error as e:
        print( e )

# trovo il prezzo di chiusura di un simbolo a una certa data
def get_price( symbol, date = None ):
    details = get_price_details( symbol, date )
    price = details['Close']
    print( 'Price for', symbol, 'on', date.strftime( '%Y-%m-%d' ), 'is', price )
    return price

# trovo i dettagli di un prezzo a una certa data
def get_price_details( symbol, date = None ):
    if date is None:
        date = datetime.datetime.today() - datetime.timedelta( days = 1 )
    else:
        date = ( datetime.datetime.strptime( date, '%Y-%m-%d' ) - datetime.timedelta( days = 1 ) ).date()
    ticker = yfinance_cache.Ticker( symbol )
    end = date + datetime.timedelta( days = 1 )
    try:
        values = ticker.history( interval = '1d', start = date, end = end )
        interval = pandas.DataFrame( values )
        closePrices = interval[ 'Close' ]
        openPrices = interval[ 'Open' ]
        closePrice = closePrices[ date.strftime( '%Y-%m-%d' ) ]
        openPrice = openPrices[ date.strftime( '%Y-%m-%d' ) ]
        print( 'Price for', symbol, 'on', date.strftime( '%Y-%m-%d' ), 'is', openPrice, '->', closePrice )
        return { 'Open': openPrice, 'Close': closePrice }
    except:
        print( 'No price found for', symbol, 'on', date.strftime( '%Y-%m-%d' ) )
        return None

# trovo la media mobile semplice di un simbolo per un periodo specifico
def get_sma( symbol, period, date = None ):
    if date is None:
        end = datetime.datetime.today()
        date = datetime.datetime.today() - datetime.timedelta( days = 1 )
    else:
        end = date
        date = ( datetime.datetime.strptime( date, '%Y-%m-%d' ) - datetime.timedelta( days = 1 ) ).date()
    ticker = yfinance_cache.Ticker( symbol )
    start = date - datetime.timedelta( days = period * 2 )
    values = ticker.history( interval = '1d', start = start, end = end )
    interval = pandas.DataFrame( values )
    if 'Close' in interval:
        close = interval[ 'Close' ]
        sma = close.rolling( window = period ).mean()
        print( 'SMA', period, 'for', symbol, 'on', date.strftime( '%Y-%m-%d' ), 'is', sma[ date.strftime( '%Y-%m-%d' ) ] )
        return sma[ date.strftime( '%Y-%m-%d' ) ]
    else:
        print( 'No price found for', symbol, 'on', date.strftime( '%Y-%m-%d' ) )
        return None

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

    # se il programma è chiamato con cinque argomenti...
    elif len( sys.argv ) == 6:
        print( '5', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] )
        if sys.argv[1] == 'get' and sys.argv[2] == 'sma':
            get_sma( sys.argv[3], int( sys.argv[4] ), sys.argv[5] )

    # se il programma è chiamato con quattro argomenti...
    elif len( sys.argv ) == 5:
        print( '4', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )
        if sys.argv[1] == 'get' and sys.argv[2] == 'price':
            get_price( sys.argv[3], sys.argv[4] )
        elif sys.argv[1] == 'get' and sys.argv[2] == 'sma':
            get_sma( sys.argv[3], int( sys.argv[4] ) )

    # se il programma è chiamato con tre argomenti...
    elif len( sys.argv ) == 4:
        print( '3', sys.argv[1], sys.argv[2], sys.argv[3] )
        if sys.argv[1] == 'advice' and sys.argv[2] == 'symbol':
            trading_advice_symbol( connection, sys.argv[3] )
        elif sys.argv[1] == 'advice' and sys.argv[2] == 'position':
            trading_advice_position( connection, sys.argv[3] )
        elif sys.argv[1] == 'get' and sys.argv[2] == 'price':
            get_price( sys.argv[3] )

    # se il programma è chiamato con due argomenti...
    elif len( sys.argv ) == 3:
        print( '2', sys.argv[1], sys.argv[2] )

    # se il programma è chiamato con un argomento...
    elif len( sys.argv ) == 2:
        print( '1', sys.argv[1] )

    # se il programma è chiamato senza argomenti...
    else:
        print( 'My Personal Trader - Trading Manager - v' + version )
        print( 'comandi disponibili:' )
        print( 'advice symbol <symbol>                                  fornisce un consiglio di trading su un simbolo' )
        print( 'advice symbol <symbol> <date>                           fornisce un consiglio di trading su un simbolo a una data specifica' )
        print( 'advice position <id>                                    fornisce un consiglio di trading su una posizione' )
        print( 'advice position <id> <date>                             fornisce un consiglio di trading su una posizione a una data specifica' )
        print( 'get price <symbol>                                      fornisce il prezzo attuale di un simbolo' )
        print( 'get price <symbol> <date>                               fornisce il prezzo di un simbolo a una data specifica' )
