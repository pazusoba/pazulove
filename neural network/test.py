from pazulove import PazuLove
from torch.utils.data import DataLoader
from dataset import TestDataset, TrainDataset
import torch

model = PazuLove(32, 16, 16, 1)
model.load_state_dict(torch.load("model.ckpt"))
model.eval()

test_loader = DataLoader(TestDataset())

# test the model
with torch.no_grad():
    correct = 0
    total = 0

    for (data, output) in test_loader:
        prediction = model(data)
        predicted, actual = prediction[0][0].item(), output.item()
        predicted_combo, actual_combo = int(predicted / 1000), int(actual / 1000)

        print("Predicted - {:.1f}, Actual - {}".format(predicted, actual))

        correct += 1 if predicted_combo == actual_combo else 0
        total += 1

    print('Accuracy: {}%'.format(100 * correct / total))
