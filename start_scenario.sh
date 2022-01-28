#!/bin/sh

sh ./end_scenario.sh

python3 load_tester.py > load_tester.log 2>&1 &
python3 pyserver.py
