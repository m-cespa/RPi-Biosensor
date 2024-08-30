import time
import numpy as np
from ds18b20 import DS18B20

order = [2, 0, 3, 1]

out_temp_sensors = DS18B20.get_all_sensors()
print(out_temp_sensors)
# ~ while True:
out_temps = []
for sensor in out_temp_sensors:
	out_temps.append(sensor.get_temperature())
out_temps = np.array(out_temps)
out_temps = out_temps[order]
print(out_temps)
