#!/usr/bin/python3

# SCRIPT PER LA GESTIONE AUTOMATICA DELLE POSIZIONI
#
# Questo script può essere chiamato dal cron di sistema e per ogni simbolo presente sulla tabella dei simboli fa una serie di
# valutazioni appoggiandosi alle strategie contenute in mpt-trading.py e in particolare:
#
# - se per un dato simbolo ci sono segnali di vendita e c'è una posizione aperta, la chiude
# - se per un dato simbolo ci sono segnali di acquisto e non c'è una posizione aperta, la apre
#
# In un secondo momento mi piacerebbe implementare anche il rinforzo delle posizioni, per cui se in un trend rialzista
# si presenta un ritracciamento il bot lo va ad acquistare nel momento in cui il trend rialzista riparte.
#
