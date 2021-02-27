"""
Used https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/01-basics/feedforward_neural_network/main.py#L37-L49 as a base
"""

from torch import nn, tensor
from torch.utils.data import DataLoader
from pazulove import PazuLove
import torch
import pandas as pd

board_size = 30

num_epochs = 3
learning_rate = 0.001

# read data from csv, get input and output data
csv_data = pd.read_csv("data/data_random.csv")
train_loader = DataLoader(csv_data.iloc[:, :-1].values, shuffle=True)
train_output = tensor(csv_data.iloc[:, -1].values, dtype=torch.float)

print("{} training data".format(len(train_output)))

# setup the model
model = PazuLove(board_size + 2, 16, 16, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    correct = 0
    total = 0

    for i, data in enumerate(train_loader):
        output = train_output[i]

        prediction = model(data.float())
        loss = criterion(prediction, output)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        predicted = int(prediction[0][0].item() / 1000)
        actual = int(output.item() / 1000)
        
        total += 1
        correct += 1 if predicted == actual else 0

        if (i + 1) % 1000 == 0:
            print ('Epoch [{} / {}], Step [{} / {}], Loss: {:.4f}, Accuracy: {:.2f}%'.format(epoch + 1, num_epochs, i + 1, total_step, loss.item(), 100 * correct / total))
            correct = 0
            total = 0

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')
