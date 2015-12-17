#!/bin/bash

cd /home/ubuntu
python fetch_data $1

./distribute_data.sh $1 $2 $4

sleep 5

./run_mtssrv.sh $3 $4

cd $3
