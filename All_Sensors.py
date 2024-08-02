# ALL_Sensors.py

import time
# import smbus2
from ds18b20 import DS18B20
from adafruit_bme280 import basic as adafruit_bme280
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_tca9548a
import numpy as np
from tqdm import tqdm

# MULTIPLEXER INITIALISATION
i2c = busio.I2C(board.SCl, board.SDA)
mux = adafruit_tca9548a.PCA9546A(i2c)

# BME280 INITIALISATION
bme_count = 4
bmes = [adafruit_bme280.Adafruit_BME280_I2C(mux[i], 0x76) for i in range(bme_count)]

# DS18B20 INITILISATION
out_temp_sensors = DS18B20.get_all_sensors()

# ADS1115 INITIALISATION
# adcs are on the same i2c bus as the mux hence same i2c argument is passed
adc_1 = ADS.ADS1115(address=0x48, i2c)
adc_2 = ADS.ADS1115(address=0x49, i2c)

channels1 = [AnalogIn(adc_1,ADS.P0),AnalogIn(adc_1,ADS.P1),
AnalogIn(adc_1,ADS.P2),AnalogIn(adc_1,ADS.P3)]

channels2 = [AnalogIn(adc_2,ADS.P0),AnalogIn(adc_2,ADS.P1),
AnalogIn(adc_2,ADS.P2),AnalogIn(adc_2,ADS.P3)]

# Script start...
duration = 10

out_file = open('data','w')
string = """t(s) T1_ext T2_ext T3_ext T4_ext 
T1 T2 T3 T4 P1 P2 P3 P4 H1 H2 H3 H4 
Turb1_180 Turb1_90 Turb2_180 Turb2_90 Turb3_180 Turb3_90 Turb4_180 Turb4_90"""
split = string.split()
title = ','.join(split)
out_file.write(title + '\n')

with tqdm(total=duration, desc="Processig: ") as pbar:
    start = time.time()
    
    while True:
    # evaluating elapsed time at loop start effectively shifts timings by ~3s
    # this sets the time-scale at regular integer stesps
        current = time.time()
        elapsed = current - start
        if elapsed > (duration+1):
            print('Data recordng complete. Terminating...')
            pbar.update(duration - pbar.n)
            break
        pbar.update(elapsed - pbar.n)
        
        start_loop = time.time()
    
        out_temps = []
        for sensor in out_temp_sensors:
            out_temps.append(sensor.get_temperature())
    # take readings from BME280 & ADS1115 after DS18B20 (faster readings)
        T_s = [bme.temperature for bme in bmes]
        P_s = [bme.pressure for bme in bmes]
        H_s = [bme.humidity for bme in bmes]
        TPH = T_s + P_s + H_s
    # adc readings for reactors 1&2 (voltages1) and reactors 3&4 (voltages2)
        voltages1 = [ch.voltage for ch in channels1]
        voltages2 = [ch.voltage for ch in channels2]
    
        line = f'{round(elapsed,3)},{",".join(map(str,out_temps))},{",".join(map(str,TPH))},{",".join(map(str,voltages1))},{",".join(map(str,voltages2))}'
        end_loop = time.time()
        diff = end_loop - start_loop
    # optional extra pause time (dt is integer by design with no pause time set)
    # pause = 10
        dt = max(np.ceil(diff),diff) - diff # + pause
        out_file.write(line + '\n')
        time.sleep(dt)
    pbar.close()
out_file.close()
