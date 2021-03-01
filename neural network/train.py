"""
Used https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/01-basics/feedforward_neural_network/main.py#L37-L49 as a base
"""

from torch import nn
from torch.utils.data import DataLoader
import torch.multiprocessing as mp
from pazulove import PazuLove
from dataset import TrainDataset
import torch
import os, sys
import time

start_time = time.time()
board_size = 30

learning_rate = 0.000001
weight_decey = 0.0001

def PAZULoss(output, target):
    loss = torch.abs((output - target))
    return loss

# setup the model
model = PazuLove(board_size + 2, 16, 8, 1)
data_percentage = 0.01
traning_data = TrainDataset(data_percentage)
train_loader = DataLoader(traning_data, shuffle=True)
criterion = nn.L1Loss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.2)
# optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decey)

model.load_state_dict(torch.load("model.ckpt"))
model.eval()

# train the model
total_step = len(train_loader)
batch_size = 100
# 10s per batch
num_iteration = batch_size * 4320
data_size = len(traning_data)

try:
    for iteration in range(num_iteration):
        correct = 0
        total = 0
        loss_total = 0

        for i, (data, output) in enumerate(train_loader):
            prediction = model(data)
            loss = PAZULoss(prediction, output)

            predicted = int(prediction[0][0].item() / 1000)
            actual = int(output.item() / 1000)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total += 1
            correct += 1 if predicted == actual else 0
            loss_total += loss.item()

        # show training info
        print ('Iteration [{} / {}], Step [{} / {}], Loss: {:.4f}, Accuracy: {:.2f}%'.format(iteration + 1, num_iteration, i + 1, total_step, loss_total / data_size, 100 * correct / total))
        correct = 0
        total = 0
        loss_total = 0
        
        # Save the model checkpoint
        torch.save(model.state_dict(), 'model.ckpt')

        if iteration % batch_size == 0:
            # update training data
            print("=== Batch {} ===".format(int(iteration / batch_size)))
            train_loader = DataLoader(TrainDataset(data_percentage))

except KeyboardInterrupt:
    print("Saving current model...")
    torch.save(model.state_dict(), 'model.ckpt')
    sys.exit(0)

# test with the same data set
with torch.no_grad():
    correct = 0
    total = 0

    for (data, output) in train_loader:
        prediction = model(data)
        predicted, actual = prediction[0][0].item(), output.item()
        predicted_combo, actual_combo = int(predicted / 1000), int(actual / 1000)

        print("Predicted - {:.1f}, Actual - {}".format(predicted, actual))

        correct += 1 if predicted_combo == actual_combo else 0
        total += 1

    print('Accuracy: {}%'.format(100 * correct / total))

# notify via email when completed, only works on certain devices
command = 'emailme "TRAINING COMPLETED" "took {}s"'.format(time.time() - start_time)
print(command)
os.system(command)
