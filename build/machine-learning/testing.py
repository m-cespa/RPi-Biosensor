import numpy as np
import temperature_model
import torch as t
import torch.nn as nn
import matplotlib.pyplot as plt

train_data = np.genfromtxt('temperature_training_1.txt', skip_header=True, delimiter=',', dtype=float)
x_data = train_data[:, :-2]
y_data = np.mean(train_data[:, -2:], axis=1)

x_data = t.from_numpy(x_data).float()
y_data = t.from_numpy(y_data).float().unsqueeze(1)

model = temperature_model.MLP()
model.load_state_dict(t.load('trained_model.pth', weights_only=True))
model.eval()

with t.no_grad():
    predictions = model(x_data)

predictions_np = predictions.cpu().numpy()
y_data_np = y_data.cpu().numpy()

plt.figure(figsize=(10, 6))
plt.plot(y_data_np, label='True Values', color='blue')
plt.plot(predictions_np, label='Model Predictions', color='orange')
plt.title('Model Predictions vs. True Values')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid()
plt.show()
