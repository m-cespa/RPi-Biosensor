import u3
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

d = u3.U3()

# Prepare data storage for plotting
max_points = 200  # Maximum number of points to display on the plot
times = []
temperatures = [[] for _ in range(1)]  

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 6))
lines = [ax.plot([], [], label=f'Sensor {i+1}')[0] for i in range(1)]
ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Real-time Temperature Data')
ax.legend()

# Function to update the plot
def update_plot():
    for i, line in enumerate(lines):
	     line.set_data(times, temperatures[i])
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
# d.getCalibrationData()
# ain2bits = d.getFeedback(u3.AIN(2))
# print(ain2bits)
# ainValue = d.binaryToCalibratedAnalogVoltage(ain2bits, isLowVoltage = False, channelNumber = 2)
start = time.time()
while True:
	ain2Value = d.getAIN(2)
	temperature = (((ain2Value-0.4)/11+0.605)*100-32)*(5/9)
	print(temperature)
	current = time.time()
	elapsed = current - start
	times.append(elapsed)
	for i in range(1):
		temperatures[i].append(temperature)
	
	# Keep only the last max_points
	if len(times) > max_points:
		times = times[-max_points:]
		for i in range(4):
			temperatures[i] = temperatures[i][-max_points:]
	# Update the plot
	update_plot()
	time.sleep(1)
