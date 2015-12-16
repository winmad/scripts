#!/bin/bash

for i in $(seq -f "%03g" 1 20)
do
    ssh node$i 'cd /home/ubuntu/; python shutdown_single.py'
done

echo "shutdown slave nodes"

cd /home/ubuntu/
python upload_data.py results.tar.gz debug.txt

echo "results uploaded, shutdown master node"

shutdown -h now