from torch.utils import data
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from PIL import Image
from pathlib import Path
import torch
import os
import random
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder
from PIL import Image
import pandas as pd

class ColorDataset(data.Dataset):
    def __init__(self, image_path: Path, transform, mode: str) -> None:
        self.image_path = image_path
        self.bw_train_path = image_path / 'trainA'
        self.color_train_path = image_path / 'trainB'

        self.bw_test_path = image_path / 'testA'
        self.color_test_path = image_path / 'testB'

        self.transform = transform
        self.mode = mode

        print ('Start preprocessing dataset..!')
        random.seed(1234)
        self.preprocess()
        print ('Finished preprocessing dataset..!')

        if self.mode == 'train':
            self.num_data = len(self.train_files)
        elif self.mode == 'test':
            self.num_data = len(self.test_files)

    def preprocess(self):
        bw_train_images = [str(x) for x in self.bw_train_path.glob('*jpg')]
        color_train_images = [str(x) for x in self.color_train_path.glob('*jpg')]

        bw_test_images = [str(x) for x in self.bw_test_path.glob('*jpg')]
        color_test_images = [str(x) for x in self.color_test_path.glob('*jpg')]

        self.train_files = bw_train_images + color_train_images
        self.train_labels = [[-1]] * len(bw_train_images) + [[1]] * len(color_train_images)

        self.test_files = bw_test_images + color_test_images
        self.test_labels = [[-1]] * len(bw_test_images) + [[1]] * len(color_test_images)


    def __getitem__(self, index):
        if self.mode == 'train':
            image = Image.open(self.train_files[index])
            label = self.train_labels[index]
        elif self.mode in ['test']:
            image = Image.open(self.train_files[index])
            label = self.test_labels[index]

        return self.transform(image), torch.FloatTensor(label)

    def __len__(self):
        return self.num_data


def get_loader(image_path: Path, crop_size: int = 256, image_size: int = 256,
        batch_size: int = 16,
        mode: str = 'train',
        num_workers: str = 1):
    """Build and return a data loader."""

    transform = []
    if mode == 'train':
        transform.append(T.RandomHorizontalFlip())
    transform.append(T.CenterCrop(crop_size))
    transform.append(T.Resize(image_size))
    transform.append(T.ToTensor())
    transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
    transform = T.Compose(transform)

    dataset = ColorDataset(image_path, transform, mode)

    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=(mode=='train'),
                                  num_workers=num_workers)
    return data_loader
