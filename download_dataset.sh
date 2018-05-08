#!/bin/bash
# https://github.com/junyanz/CycleGAN/blob/master/datasets/download_dataset.sh

FILE=$1

DATASETS=(\
    apple2orange\
    summer2winter_yosemite\
    horse2zebra\
    monet2photo\
    cezanne2photo\
    ukiyoe2photo\
    vangogh2photo\
    maps\
    cityscapes\
    facades\
    iphone2dslr_flower\
    ae_photos\
    )


found=false

for d in ${DATASETS[@]}; do
    if [[ "$d" == "$FILE" ]]; then
        found=true
    fi
done

if ! $found; then
    echo "Available datasets: ${DATASETS[@]}"
    exit 1
fi

URL=https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/$FILE.zip
ZIP_FILE=./data/$FILE.zip
TARGET_DIR=./data/$FILE/
mkdir -p $TARGET_DIR
wget -c $URL -O $ZIP_FILE
unzip -u $ZIP_FILE -d ./data/
