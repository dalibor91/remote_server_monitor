#!/bin/bash 


docker build -t monitor .

docker run -it --rm -v "`pwd`/server:/server" -p "8765:8765" monitor bash 

