#!/bin/bash

# librerie
sudo apt-get install python3-pandas
pipx install yahoo-finance
pipx install yahoo-finance-cache

# inizializzazione database
./mpt-db.py init
