#~/bin/bash

for i in $(seq -f "%03g" 1 20)
do
    ssh node$i 'cd /home/ubuntu/; python distribute_data_single.py gabardine_albedo.tar.gz /mnt/gabardine/'
done