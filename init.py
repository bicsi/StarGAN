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
        from PIL import Image
        img = Image.open(src).convert('LA').convert('RGB')
        img.save(dst)

    for d1 in ['train', 'test']:
        force_make(rafd / d1)
        for d2 in ['bw', 'color']:
            force_make(rafd / d1 / d2)

    it = 0
    for f in test:
        if it % 2 == 0:
            shutil.copy(str(f), str(rafd / 'test' / 'color'))
        else:
            conv(str(f), str(rafd / 'test' / 'bw' / f.name))
        it += 1
    for f in train:
        if it % 2 == 0:
            shutil.copy(str(f), str(rafd / 'train' / 'color'))
        else:
            conv(str(f), str(rafd / 'train' / 'bw' / f.name))
        it += 1

    for filename in os.listdir(str(rafd)):
      if filename.endswith('.jpg'):
        os.unlink(str(rafd / filename))

def main():
    download_all()
    make_comp()
    partition()



if __name__ == '__main__':
    main()
