#!/bin/sh 
# A simple script to remove old test images and prepare new ones.

cd $(dirname $0)
for file_type in *; do 
    if [ -d "$file_type" ]; then
        rm -f ${file_type}/test/* 
        cp ${file_type}/*.${file_type} ${file_type}/test/image
    fi 
done
