import time
from ds18b20 import DS18B20
from adafruit_bme280 import basic as adafruit_bme280
import board
import busio
import adafruit_tca9548a


#MULTIPLEXER INITIALISATION
i2c = busio.I2C(board.SCL, board.SDA)
mux = adafruit_tca9548a.PCA9546A(i2c)

# BME280 INITIALISATION
bme_count = 4
bmes = [adafruit_bme280.Adafruit_BME280_I2C(mux[i], 0x76) for i in range(bme_count)]

while True:
		T_s = [bme.temperature for bme in bmes]
		P_s = [bme.pressure for bme in bmes]
		H_s = [bme.humidity for bme in bmes]
		TPH = T_s + P_s + H_s
		print(TPH)
