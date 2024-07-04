#!/bin/bash

path=$(hostname -I)

echo " The ip-address of server on your local network is https://"+$path+":5000 "

python3 "./server.py" &
python3 "./variable_server.py"