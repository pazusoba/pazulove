"""
Used https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/01-basics/feedforward_neural_network/main.py#L37-L49 as a base
"""

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

        # self.relu = nn.ReLU()
        self.activation = nn.Sigmoid()
        # self.softmax = nn.Softmax(dim=1)

    def forward(self, out):
        out = self.hidden1(out)
        out = self.activation(out)

        out = self.hidden2(out)
        out = self.activation(out)

        out = self.output(out)
        # out = self.softmax(out)
        return out


board_size = 30

num_epochs = 200
learning_rate = 0.01

# read data from csv, get input and output data
csv_data = pd.read_csv("../data/data_random.csv")
data_size = len(csv_data)
train_index = int(data_size * 0.9)
train_loader = DataLoader(csv_data.iloc[:train_index, :-1].values)
train_output = tensor(csv_data.iloc[:train_index, -1].values, dtype=torch.float)

# 1000 data for testing
test_index = -(data_size - train_index)
test_loader = DataLoader(csv_data.iloc[test_index:, :-1].values)
test_output = tensor(csv_data.iloc[test_index:, -1].values, dtype=torch.float)

print("training: {}, testing: {}".format(len(train_output), len(test_output)))

# setup the model
model = PazuLove(board_size + 2, 16, 8, 1)
criterion = nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  

# train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, data in enumerate(train_loader):
        output = train_output[i]

        prediction = model(data.float())
        loss = criterion(prediction, output)

        # backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i + 1) % 10 == 0:
            print ('Epoch [{} / {}], Step [{} / {}], Loss: {:.0f}'.format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

# test the model
with torch.no_grad():
    correct = 0
    total = 0

    for i, data in enumerate(test_loader):
        output = test_output[i]

        prediction = model(data.float())
        predicted = int(prediction[0][0].item() / 1000)
        actual = int(output.item() / 1000)

        correct += 1 if predicted == actual else 0
        total += 1

    print('Accuracy: {}%'.format(100 * correct / total))

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')
