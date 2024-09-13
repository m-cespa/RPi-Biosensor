import adafruit_pct2075
import board
import busio
from ds18b20 import DS18B20
import numpy as np

# DS18B20 INITILISATION
order = [2, 0, 3, 1]
out_temp_sensors = np.array(DS18B20.get_all_sensors())
out_temp_sensors = out_temp_sensors[order]

i2c = busio.I2C(board.SCL, board.SDA)
pct = adafruit_pct2075.PCT2075(i2c)
print("Temperature: %.2f C"%pct.temperature)
out_temps = []
out_temps.append(pct.temperature)
for sensor in out_temp_sensors:
	out_temps.append(sensor.get_temperature())
print(out_temps)
