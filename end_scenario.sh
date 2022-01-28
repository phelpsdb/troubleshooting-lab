#!/bin/sh

kill $(ps aux | grep 'python3 load_tester.py' | grep -v 'grep' | awk '{print $2}') >/dev/null 2>&1
kill -1 $(ps aux | grep 'python3 pyserver.py' | grep -v 'grep' | awk '{print $2}') >/dev/null 2>&1
