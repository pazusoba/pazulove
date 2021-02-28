from torch.utils.data import Dataset, DataLoader
import pandas as pd
import torch

class BaseDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv("../{}".format(csv_file))
        self.iterator = iter(self[x] for x in range(len(self)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        curr = self.data.iloc[index].values
        # convert to tensor and float type
        return (torch.tensor(curr[:-1], dtype=torch.float), torch.tensor(curr[-1], dtype=torch.float))

    def __iter__(self):
        return self.iterator

class TrainDataset(BaseDataset):
    """
    loaded from data_random.csv
    """
    def __init__(self):
        super().__init__("data/data_random.csv")

class TestDataset(BaseDataset):
    """
    loaded from data_test.csv
    """
    def __init__(self):
        super().__init__("data/data_test.csv")

class SmallDataSet(BaseDataset):
    """
    loaded from data_small.csv
    """
    def __init__(self):
         super().__init__("data/data_small.csv")

# test
# train = TestDataset()
# (first, second) = train[0]
# print(first, second)
# print(len(train))
# for i in train:
#     pass