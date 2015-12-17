Usage:

python fetch_data.py <tar file in S3>
python fetch_data.py bunny.tar.gz

./distribute_data.sh <tar file> <data directory> <#slave nodes>
./distribute_data.sh bunny.tar.gz /mnt/ 9

./run_mtssrv.sh <data directory> <#slave nodes>
./run_mtssrv.sh /mnt/bunny 9

python upload_data.py <tar file> <result directory>
python upload_data.py results.tar.gz /mnt/bunny/results

./shutdown.sh <tar file> <result directory> <#slave nodes>
./shutdown.sh results.tar.gz /mnt/bunny/results 9