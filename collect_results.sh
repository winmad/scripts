#!/bin/bash

for i in $(seq -f "%03g" 1 $2)
do
    ssh node$i "rm $1image_*"
    ssh node$i "scp $1*.pfm master:$1tmp/"
    ssh node$i "rm $1*.pfm"
done
