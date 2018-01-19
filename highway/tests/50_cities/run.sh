#!/usr/bin/env bash

./../../main.py cities 50 3 -s 10 > 10steps
./../../main.py cities 50 3 -s 100 > 100steps
./../../main.py cities 50 3 -s 1000 > 1000steps
./../../main.py cities 50 3 -s 10000 > 10000steps
