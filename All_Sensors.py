import time
import smbus2
from ds18b20 import DS18B20
from adafruit_bme280 import basic as adafruit_bme280
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_tca9548a
import numpy as np

# MULTIPLEXER INITIALISATION
i2c = board.I2C()
mux = adafruit_tca9548a.PCA9546A(i2c)

# BME280 INITIALISATION
bme_count = 4
bmes = [adafruit_bme280.Adafruit_BME280_I2C(mux[i], 0x76) for i in range(bme_count)]

# DS18B20 INITILISATION
out_temp_sensors = DS18B20.get_all_sensors()

# ADS1115 INITIALISATION
ads_ad = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(ads_ad)

channels = [AnalogIn(ads,ADS.P0),AnalogIn(ads,ADS.P1),
AnalogIn(ads,ADS.P2),AnalogIn(ads,ADS.P3)]

# Script start...
duration = 10

out_file = open('data','w')
string = 't(s) T1_ext T2_ext T1 T2 T3 T4 P1 P2 P3 P4 H1 H2 H3 H4 Turb1 Turb2 Turb3 Turb4'
split = string.split()
title = ','.join(split)
out_file.write(title + '\n')

start = time.time()
while True:
# evaluating elapsed time at loop start effectively shifts timings by ~2s
# this sets the time-scale at regular integer stesps
    current = time.time()
    elapsed = current - start
    if elapsed > (duration+1):
        print('Data recordng complete. Terminating...')
        break

    start_loop = time.time()

    out_temps = []
    for sensor in out_temp_sensors:
        out_temps.append(sensor.get_temperature())
# take readings from BME280 & ADS1115 after DS18B20 (faster readings)
    T_s = [bme.temperature for bme in bmes]
    P_s = [bme.pressure for bme in bmes]
    H_s = [bme.humidity for bme in bmes]
    TPH = T_s + P_s + H_s
    voltages = [ch.voltage for ch in channels]

    line = f'{round(elapsed,3)},{",".join(map(str,out_temps))},{",".join(map(str,TPH))},{",".join(map(str,voltages))}'
    end_loop = time.time()
    diff = end_loop - start_loop
    dt = max(np.ceil(diff),diff) - diff
    out_file.write(line + '\n')
    time.sleep(dt)
out_file.close()