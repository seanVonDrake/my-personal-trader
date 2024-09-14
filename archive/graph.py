import os
import sys
import pandas
import yfinance
import yfinance_cache
import finplot
import datetime
import numpy
import matplotlib.pyplot
import cv2

if __name__ == '__main__':

    if len( sys.argv ) == 3:

        symbol = sys.argv[1]
        date = datetime.datetime.strptime( sys.argv[2], '%Y-%m-%d' ).date()
        start = date - datetime.timedelta( days = 365 )

        ticker = yfinance_cache.Ticker( symbol )
        data = ticker.history( interval = '1d', start = start, end = date )

        interval = pandas.DataFrame( data )

        close = interval[ 'Close' ]

        sma10 = close.rolling( window = 10 ).mean()
        sma20 = close.rolling( window = 20 ).mean()
        sma30 = close.rolling( window = 30 ).mean()

        matplotlib.use( 'GTK3Agg' )
        matplotlib.pyplot.title( 'three MA strategy (10,20,30) for $' + symbol )
        matplotlib.pyplot.fill_between( close.index, 0, close, alpha=0.3 )
        matplotlib.pyplot.plot( close )
        matplotlib.pyplot.plot( sma10 )
        matplotlib.pyplot.plot( sma20 )
        matplotlib.pyplot.plot( sma30 )
        matplotlib.pyplot.show()

        # finplot.candlestick_ochl( interval[ ['Open','Close','High','Low'] ] )
        # finplot.show()
