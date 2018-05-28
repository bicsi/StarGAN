#!/usr/bin/env python3
import os
import shutil
import subprocess
from random import randint, shuffle
from pathlib import Path

datasets = [
    'apple2orange',
    'summer2winter_yosemite',
    # 'horse2zebra',
    # 'monet2photo',
    # 'cezanne2photo',
]


def download_all():
    for d in datasets:
        subprocess.run(['bash', 'download_dataset.sh', d], check=True)


def force_make(path: Path):
    if path.exists():
        shutil.rmtree(str(path))
    path.mkdir()


def make_comp():
    comp = Path('data/rafd')
    force_make(comp)

    for d in datasets:
        dpath = Path('data') / d
        for img in dpath.glob('**/*.jpg'):
            shutil.copy(str(img), str(comp))


def partition():
    rafd = Path('data/rafd')
    images = list(rafd.glob('*.jpg'))
    shuffle(images)

    N = len(images)
    ntest = int(N * 0.1)
    ntrain = N - ntest

    test = images[: ntest]
    train = images[ntest:]

    assert len(test) == ntest
    assert len(train) == ntrain

    def conv(src: str, dst: str):
        print('Converting {}'.format(src))
        subprocess.run(['convert', src, '-colorspace', 'Gray', dst], check=True)
        subprocess.run(['convert', dst, '-colorspace', 'sRGB', '-type', 'truecolor', dst], check=True)

    for d1 in ['train', 'test']:
        force_make(rafd / d1)
        for d2 in ['bw', 'color']:
            force_make(rafd / d1 / d2)

    for f in test:
        shutil.copy(str(f), str(rafd / 'test' / 'color'))
        conv(str(f), str(rafd / 'test' / 'bw' / f.name))
    for f in train:
        shutil.copy(str(f), str(rafd / 'train' / 'color'))
        conv(str(f), str(rafd / 'train' / 'bw' / f.name))


def main():
    download_all()
    make_comp()
    partition()


if __name__ == '__main__':
    main()
