from random import randint
from typing import Tuple

import torch

from python_code.utils.config_singleton import Config

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

conf = Config()


class RandomSampler:
    """
    The proposed augmentations scheme. Calculates centers and variances for each class as specified in the paper,
    then smooths the estimate via a window running mean with alpha = 0.3
    """

    def __init__(self, received_words: torch.Tensor, transmitted_words: torch.Tensor, gt_states: torch.Tensor):
        super().__init__()
        self._received_words = received_words
        self._transmitted_words = transmitted_words
        self._states = gt_states

    def sample(self, to_augment_state: int, h: torch.Tensor, snr: float) -> Tuple[torch.Tensor, torch.Tensor]:
        random_ind = randint(a=0, b=self._received_words.shape[0] - 1)
        x, y = self._received_words[random_ind].reshape(1, -1), self._transmitted_words[random_ind].reshape(1, -1)
        return x, y