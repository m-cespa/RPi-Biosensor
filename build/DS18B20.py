from ds18b20 import DS18B20
import time
import numpy as np

order = [2, 0, 3, 1]
sensors = DS18B20.get_all_sensors()
sensors = np.array(sensors)
sensors = sensors[order]

while True:
	out_temps = []
	for sensor in sensors:
		out_temps.append(sensor.get_temperature())
	# ~ out_temps = np.array(out_temps)
	# ~ out_temps = out_temps[order]

	print(out_temps)
	
