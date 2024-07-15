import time
import smbus2
import bme280

# BME280 sensor address
ad = 0x76

# initialising I2C bus
bus = smbus2.SMBus(1)

# load calibration parameters
calib_params = bme280.load_calibration_params(bus, ad)

duration = 10
dt = 1

out_file = open('BME280_data','w')
out_file.write('Time(s)'+','+'Temperature'+','+'Pressure'+'Humidity'+'\n')

start_time = time.time()
while True:
	current_time = time.time()
	elapsed_time = current_time - start_time
	if elapsed_time >= (duration + dt):
		print('Data recordng complete. Terminating...')
		break
	data = bme280.sample(bus, ad, calib_params)
	line = f'{round(elapsed_time,3)}'
	line += f',{str(data.temperature)},{str(data.pressure)},{str(data.humidity)}'

	out_file.write(line + '\n')
	time.sleep(dt)
out_file.close()