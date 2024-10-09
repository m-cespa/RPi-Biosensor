import numpy as np
import temperature_model
import torch as t
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import tqdm

# import data and averaging over flask temperatures
train_data = np.genfromtxt('temperature_training_1.txt', skip_header=True, delimiter=',', dtype=float)
x_data = train_data[:, :-2]
y_data = np.mean(train_data[:, -2:], axis=1)

x_data = t.from_numpy(x_data).float()
y_data = t.from_numpy(y_data).float().unsqueeze(1)

device = t.device("cuda" if t.cuda.is_available() else "cpu")

class TrainingArgs():
    epochs: int = 100
    learning_rate: float = 0.0005
    batch_size: int = 50

def prepare_data_loader(X_train, y_train, batch_size):
    dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(dataset, batch_size, shuffle=True)
    return train_loader

def train(args: TrainingArgs):
    model = temperature_model.MLP().to(device)

    # adjusting weight_decay for smoothing purposes
    optimizer = t.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=1e-10)
    criterion = nn.MSELoss()
    train_loader = prepare_data_loader(x_data, y_data, batch_size=args.batch_size)

    for epoch in tqdm.tqdm(range(args.epochs)):
        total_loss = 0

        for inputs, temperature in train_loader:
            inputs, temperature = inputs.to(device), temperature.to(device)

            optimizer.zero_grad()
            logits = model(inputs)
            loss = criterion(logits, temperature)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch [{epoch + 1}/{args.epochs}], Loss: {total_loss / len(train_loader):.4f}")

    t.save(model.state_dict(), 'trained_model.pth')

train(TrainingArgs)

