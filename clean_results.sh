#!/bin/bash

for i in $(seq -f "%03g" 1 $2)
do
    ssh node$i "rm $1*.pfm"
done

rm *.pfm
rm tmp/*.pfm
