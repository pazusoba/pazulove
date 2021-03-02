from torch import nn

class PazuLove(nn.Module):
    """
    A neural network with 2 hidden layers
    """

    def __init__(self, input_count, hidden1_count, hidden2_count, output_count):
        super().__init__()

        # input, hidden1, hidden2 and output
        self.hidden1 = nn.Linear(input_count, hidden1_count)
        # self.hidden2 = nn.Linear(hidden1_count, hidden2_count)
        self.output = nn.Linear(hidden1_count, output_count)

        self.activation = nn.ReLU()

    def forward(self, out):
        out = self.hidden1(out)
        out = self.activation(out)

        # out = self.hidden2(out)
        # out = self.activation(out)

        out = self.output(out)
        return out
