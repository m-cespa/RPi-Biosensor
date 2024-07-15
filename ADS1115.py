import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# ADS1115 INITIALISATION
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

channels = [AnalogIn(ads,ADS.P0),AnalogIn(ads,ADS.P1),
AnalogIn(ads,ADS.P2),AnalogIn(ads,ADS.P3)]

voltages = [ch.voltage for ch in channels]

print(voltages[0])