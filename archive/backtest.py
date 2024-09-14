import os
import sys
import datetime

if __name__ == '__main__':

    if len( sys.argv ) == 3:
        
        start = datetime.datetime.strptime( sys.argv[1], '%Y-%m-%d' ).date()
        stop = datetime.datetime.strptime( sys.argv[2], '%Y-%m-%d' ).date()
        now = start

        while now <= stop:
            print( 'test per il giorno', now )
            now += datetime.timedelta( days = 1 )
            os.system( 'python3 mypersonaltrader.py ' + now.strftime( '%Y-%m-%d' ) )
