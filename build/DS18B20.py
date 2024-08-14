from ds18b20 import DS18B20
import time

sensors = DS18B20.get_all_sensors()

start = time.time()
for sensor in sensors:
	print(f'Sensor has temperature {(sensor.get_id(), sensor.get_temperature())}')

end = time.time()
diff = end - start
print(f'\n {diff}')
