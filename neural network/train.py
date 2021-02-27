from torch import nn, tensor
from torch.utils.data import DataLoader
import torch
import pandas as pd

class PazuLove(nn.Module):
    """
    A neural network with 2 hidden layers
    """

    def __init__(self, input_count, hidden1_count, hidden2_count, output_count):
        super().__init__()

        # input, hidden1, hidden2 and output
        self.hidden1 = nn.Linear(input_count, hidden1_count)
        self.hidden2 = nn.Linear(hidden1_count, hidden2_count)
        self.output = nn.Linear(hidden2_count, output_count)

        self.relu = nn.ReLU()
        self.activation = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, out):
        out = self.hidden1(out)
        out = self.relu(out)

        out = self.hidden2(out)
        out = self.relu(out)

        out = self.output(out)
        out = self.softmax(out)
        return out


board_size = 30

num_epochs = 20
batch_size = 1000
learning_rate = 0.01

# read data from csv, get input and output data
csv_data = pd.read_csv("data/data_100.csv")
input_loader = DataLoader(csv_data.iloc[:, :-1].values)
output_data = tensor(csv_data.iloc[:, -1].values, dtype=torch.float)

# setup the model
model = PazuLove(board_size + 2, 16, 8, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  

# train the model
total_step = len(input_loader)
for epoch in range(num_epochs):
    for i, data in enumerate(input_loader):
        output = output_data[i]

        prediction = model(tensor(data, dtype=torch.float))
        loss = criterion(prediction, output)
        
        # backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print ('Epoch [{} / {}], Step [{} / {}], Loss: {:.4f}'.format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))
