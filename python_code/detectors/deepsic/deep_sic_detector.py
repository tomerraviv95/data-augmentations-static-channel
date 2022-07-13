import torch
from torch import nn

from python_code.channel.channels_hyperparams import N_USER, N_ANT, MODULATION_NUM_MAPPING
from python_code.utils.config_singleton import Config

conf = Config()

CLASSES_NUM = MODULATION_NUM_MAPPING[conf.modulation_type]
HIDDEN_SIZE = 60


class DeepSICDetector(nn.Module):
    """
    The DeepSIC Network Architecture

    ===========Architecture=========
    DeepSICNet(
      (fullyConnectedLayer): Linear(in_features=s_nK+s_nN-1, out_features=60, bias=True)
      (sigmoid): Sigmoid()
      (fullyConnectedLayer): Linear(in_features=60, out_features=30, bias=True)
      (reluLayer): ReLU()
      (fullyConnectedLayer2): Linear(in_features=30, out_features=2, bias=True)
    ================================
    Note:
    The output of the network is not probabilities,
    to obtain probabilities apply a softmax function to the output, viz.
    output = DeepSICNet(data)
    probs = torch.softmax(output, dim), for a batch inference, set dim=1; otherwise dim=0.
    """

    def __init__(self):
        super(DeepSICDetector, self).__init__()
        linear_input = (MODULATION_NUM_MAPPING[conf.modulation_type] // 2) * N_ANT + (
                    MODULATION_NUM_MAPPING[conf.modulation_type] - 1) * (N_USER - 1)
        self.fc0 = nn.Linear(linear_input, HIDDEN_SIZE)
        self.sigmoid = nn.Sigmoid()
        self.fc1 = nn.Linear(HIDDEN_SIZE, int(HIDDEN_SIZE / 2))
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(int(HIDDEN_SIZE / 2), CLASSES_NUM)

    def forward(self, y: torch.Tensor) -> torch.Tensor:
        out0 = self.sigmoid(self.fc0(y.squeeze(-1)))
        fc1_out = self.relu(self.fc1(out0))
        out = self.fc2(fc1_out)
        return out
