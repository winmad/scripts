#!/bin/bash

for i in $(seq -f "%03g" 1 1)
do
    ssh node$i 'cd /home/ubuntu/; screen -d -m ./run_mtssrv_single.sh'
done