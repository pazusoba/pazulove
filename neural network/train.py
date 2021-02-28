"""
Used https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/01-basics/feedforward_neural_network/main.py#L37-L49 as a base
"""

from torch import nn, tensor
from torch.utils.data import DataLoader
from pazulove import PazuLove
from dataset import TrainDataset, SmallDataSet
import torch
import os, time

start_time = time.time()
board_size = 30

num_epochs = 10000
learning_rate = 0.0001

def PAZULoss(output, target):
    # target / 1000 == output / 1000
    # print(target - output)
    loss = torch.mean((output / 1000 - target / 1000) ** 2)
    return loss

# setup the model
model = PazuLove(board_size + 2, 16, 16, 1)
train_loader = DataLoader(TrainDataset(), shuffle=True)
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    correct = 0
    total = 0

    for i, (data, output) in enumerate(train_loader):
        prediction = model(data)
        loss = PAZULoss(prediction, output)

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

# notify via email when completed, only works on certain devices
command = 'emailme "TRAINING COMPLETED" "took {}s"'.format(time.time() - start_time)
print(command)
os.system(command)
