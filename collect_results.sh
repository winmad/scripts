#!/bin/bash

for i in $(seq -f "%03g" 1 $2)
do
    ssh node$i "cd $1; scp $1*.pfm master:$1"
    ssh node$i "rm $1*.pfm"
done
