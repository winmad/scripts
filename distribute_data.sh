#!/bin/bash

for i in $(seq -f "%03g" 1 $3)
do
    ssh node$i 'cd /home/ubuntu/; python distribute_data_single.py $1 $2'
done

cd /home/ubuntu/
python distribute_data_single.py $1 $2
