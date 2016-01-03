#!/bin/bash

if [ $# != 4 ]
then
    echo "need parameters!"
    exit 1
fi

cd /home/ubuntu
#python fetch_data.py $1

./distribute_data.sh $1 $2 $4

sleep 5

./run_mtssrv.sh $3 $4

. /home/ubuntu/mitsuba/setpath.sh

cd $3
