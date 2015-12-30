#!/bin/bash

for i in $(seq -f "%03g" 1 $2)
do
    ssh node$i "screen -X quit"
    ssh node$i "cd /home/ubuntu/; screen -d -m ./run_mtssrv_single.sh $1"
done