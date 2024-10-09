import numpy as np
import einops
import torch as t
from torch import Tensor
import torch.nn as nn

t.manual_seed(4)

class ReLU(nn.Module):
    def forward(self, x: Tensor) ->  Tensor:
        return t.max(t.tensor(0.), x)
    
class Linear(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias=True):
        """Linear transformation with dimensionality change"""
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias

        limit = 1/np.sqrt(in_features)

        # initialise weights as random distribution on [-1,1]
        # normalise by number of input features
        weight = limit * (2 * t.rand(out_features, in_features) - 1)
        self.weight = nn.Parameter(weight)

        if bias:
            # trailing comma to signify tensor status although just a vector
            # also initialised to a normalised uniform on [-1,1]
            bias = limit * (2 * t.rand(out_features,) - 1)
            self.bias = nn.Parameter(bias)
        else:
            self.bias = None

    def forward(self, x: Tensor) -> Tensor:
        """
        x shape: (*, in_features)
        out shape: (*, out_features)
        """
        x = einops.einsum(x, self.weight, '... in_feats, out_feats in_feats -> ... out_feats')

        if self.bias is not None:
            x += self.bias

        return x
    
class Normalisation(nn.Module):
    def __init__(self, mean, std):
        super().__init__()
        # register the mean and std as buffers
        self.register_buffer('mean', t.tensor(mean))
        self.register_buffer('std', t.tensor(std))

    def forward(self, x):
        return (x - self.mean) / self.std
    
class DeNormalisation(nn.Module):
    def __init__(self, mean, std):
        super().__init__()
        # register the mean and std as buffers
        self.register_buffer('mean', t.tensor(mean))
        self.register_buffer('std', t.tensor(std))

    def forward(self, x):
        return x * self.std + self.mean
    
class SmoothingConv1D(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, kernel_size=5, padding=2, stride=1):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, padding=padding, stride=stride)

        # averaging kernel initialised
        with t.no_grad():
            kernel = t.ones(out_channels, in_channels, kernel_size) / kernel_size
            self.conv.weight.copy_(kernel)

    def forward(self, x: t.Tensor) -> t.Tensor:
        return self.conv(x)

class Sequential(nn.Module):
    _modules: dict[str, nn.Module]

    def __init__(self, *modules: nn.Module):
        super().__init__()
        for index, mod in enumerate(modules):
            self._modules[str(index)] = mod

    def __getitem__(self, index: int) -> nn.Module:
        index %= len(self._modules) # deal with negative indices
        return self._modules[str(index)]

    def __setitem__(self, index: int, module: nn.Module) -> None:
        index %= len(self._modules) # deal with negative indices
        self._modules[str(index)] = module

    def forward(self, x: t.Tensor) -> t.Tensor:
        for mod in self._modules.values():
            x = mod(x)
        return x

class MLP(nn.Module):
    def __init__(self, input_dim=3, hidden_dim=32, input_mean=0., input_std=1.):
        super().__init__()

        self.stream = Sequential(
            Normalisation(mean=input_mean, std=input_std),
            Linear(input_dim, hidden_dim),
            ReLU(),
            Linear(hidden_dim, hidden_dim // 2),
            ReLU(),
            Linear(hidden_dim // 2, hidden_dim // 4),
            ReLU(),
            Linear(hidden_dim // 4, 1),
            ReLU(),
            DeNormalisation(mean=input_mean, std=input_std),
        )

        # expecting input of shape: (batch_size=20, channels=1)
        self.smoothing = SmoothingConv1D(in_channels=1, out_channels=1)

    def forward(self, x: Tensor) -> Tensor:
        x = self.stream(x)  # Shape is (batch_size, 1)

        # reshape for Conv1D required
        # shape now: (batch_size, channels=1, sequence_length=1)
        x = x.unsqueeze(1)
        x = self.smoothing(x)

        # squeeze the added dimension
        return x.squeeze(1)
