from torch import nn
import pandas as pd

input_size = 32
hiden_layers = [16, 8]
output_size = 1

# a neural network with 2 hidden layers
model = nn.Sequential(
    nn.Linear(input_size, hiden_layers[0]),
    nn.ReLU(),
    nn.Linear(hiden_layers[0], hiden_layers[1]),
    nn.ReLU(),
    nn.Linear(hiden_layers[1], output_size),
    nn.Softmax(dim=1)
)

# read data from csv
board_data = pd.read_csv("data/data_random.csv")
output_score = board_data.iloc[:, -1].values
print(output_score)
