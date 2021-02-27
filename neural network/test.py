from pazulove import PazuLove
from torch.utils.data import DataLoader
import torch
import pandas as pd

model = PazuLove(32, 16, 16, 1)
model.load_state_dict(torch.load("model.ckpt"))
model.eval()

# csv_data = pd.read_csv("data/data_random.csv")
csv_data = pd.read_csv("data/data_100.csv")

test_loader = DataLoader(csv_data.iloc[:, :-1].values)
test_output = torch.tensor(csv_data.iloc[:, -1].values, dtype=torch.float)

# test the model
with torch.no_grad():
    correct = 0
    total = 0

    for i, data in enumerate(test_loader):
        output = test_output[i]

        prediction = model(data.float())
        predicted, actual = prediction[0][0].item(), output.item()
        predicted_combo, actual_combo = int(predicted / 1000), int(actual / 1000)

        print("Predicted - {}, Actual - {}".format(predicted, actual))

        correct += 1 if predicted_combo == actual_combo else 0
        total += 1

    print('Accuracy: {}%'.format(100 * correct / total))
