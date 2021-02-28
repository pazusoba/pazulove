"""
Used https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/01-basics/feedforward_neural_network/main.py#L37-L49 as a base
"""

from torch import nn, tensor
from torch.utils.data import DataLoader
from pazulove import PazuLove
from dataset import TrainDataset, SmallDataSet
import torch
import os, time, sys

start_time = time.time()
board_size = 30

num_epochs = 5000
learning_rate = 0.00001

def PAZULoss(output, target):
    # target / 1000 == output / 1000
    # print(target - output)
    loss = torch.mean((output / 1000 - target / 1000) ** 2)
    return loss

# setup the model
model = PazuLove(board_size + 2, 16, 8, 1)
traning_data = TrainDataset(0.1)
train_loader = DataLoader(traning_data, shuffle=True)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

# train the model
total_step = len(train_loader)
batch_size = len(traning_data)

try:
    for epoch in range(num_epochs):
        correct = 0
        total = 0
        loss_total = 0

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
            loss_total += loss.item()

            if (i + 1) % batch_size == 0:
                print ('Epoch [{} / {}], Step [{} / {}], Loss: {:.4f}, Accuracy: {:.2f}%'.format(epoch + 1, num_epochs, i + 1, total_step, loss_total / batch_size, 100 * correct / total))
                correct = 0
                total = 0
                loss_total = 0
except KeyboardInterrupt:
    print("Saving current model...")
    torch.save(model.state_dict(), 'model.ckpt')
    sys.exit(0)

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')

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
