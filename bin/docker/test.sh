#!/bin/bash 

bin/service start 

cd test
python3 -m unittest discover --pattern=*.py
