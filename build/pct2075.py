import adafruit_pct2075
import board
import busio
from ds18b20 import DS18B20
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

inputs = [1]
# Prepare data storage for plotting
times = []
outputs = [[] for _ in range(len(inputs))]  

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 6))
lines = [ax.plot([], [], label=f'Sensor {i+1}')[0] for i,_ in enumerate(inputs)]
ax.set_xlabel('Time (h)')
# ax.set_ylabel('Temperature (°C)')
ax.set_title('Real-time Temperature Data')
ax.legend(loc=3,fontsize=8,bbox_to_anchor=(0.2, 0.2))


def update_plot():
    for i, line in enumerate(lines):
	     line.set_data(times, outputs[i])
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
# DS18B20 INITILISATION
order = [2, 0, 3, 1]
out_temp_sensors = np.array(DS18B20.get_all_sensors())
out_temp_sensors = out_temp_sensors[order]

i2c = busio.I2C(board.SCL, board.SDA)
pct = adafruit_pct2075.PCT2075(i2c)
print("Temperature: %.2f C"%pct.temperature)
start = time.time()

while True:
	current = time.time()
	elapsed = (current - start)/3600
	times.append(elapsed)
	out_temps = []
	out_temps.append(pct.temperature)
	for i, temp in enumerate(out_temps):
		outputs[i].append(temp)
	update_plot()
	time.sleep(1)
