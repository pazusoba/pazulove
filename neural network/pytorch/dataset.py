from torch.utils.data import Dataset, DataLoader
import pandas as pd
import torch


class BaseDataset(Dataset):
    def __init__(self, csv_file, max_size=0):
        csv_data = pd.read_csv("../{}".format(csv_file))
        if max_size <= 0:
            # use everything
            self.data = csv_data
        else:
            self.data = csv_data.sample(frac=max_size)
        self.iterator = iter(self[x] for x in range(len(self)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        curr = self.data.iloc[index].values
        # convert to tensor and float type
        return (torch.tensor(curr[:-1], dtype=torch.float, requires_grad=True), torch.tensor(curr[-1], dtype=torch.float))

    def __iter__(self):
        return self.iterator


class TrainDataset(BaseDataset):
    """
    loaded from data8_random.csv
    """

    def __init__(self, max_size=0):
        super().__init__("data/data8_random.csv", max_size)


class TestDataset(BaseDataset):
    """
    loaded from data8_test.csv
    """

    def __init__(self, max_size=0):
        super().__init__("data/data8_test.csv", max_size)


class SmallDataset(BaseDataset):
    """
    loaded from data8_small.csv
    """

    def __init__(self):
        super().__init__("data/data8_small.csv")

# test
# train = TestDataset()
# (first, second) = train[0]
# print(first, second)
# print(len(train))
# for i in train:
#     pass
