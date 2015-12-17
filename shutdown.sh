#!/bin/bash

for i in $(seq -f "%03g" 1 $3)
do
    ssh node$i 'cd /home/ubuntu/; python shutdown_single.py'
done

echo "shutdown slave nodes"

cd /home/ubuntu/
python upload_data.py $1 $2

echo "results uploaded, shutdown master node"

#shutdown -h now