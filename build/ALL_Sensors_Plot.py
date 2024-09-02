import time
from ds18b20 import DS18B20
from adafruit_bme280 import basic as adafruit_bme280
import board
import busio
import adafruit_ads1x15.ads1115 as ADS_1
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads7830.ads7830 as ADS_2
import adafruit_tca9548a
import RPi.GPIO as IO
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Setup GPIO
IO.setmode(IO.BCM)  # Set the GPIO mode to BOARD numbering
LED_Pin = 26  # Define the pin number for the LED
IO.setup(LED_Pin, IO.OUT)  # Set the LED_Pin as an output pin

# MULTIPLEXER INITIALISATION
i2c = busio.I2C(board.SCL, board.SDA)
mux = adafruit_tca9548a.PCA9546A(i2c)

# ADS1115 INITIALISATION
# through beam readings
adc_1 = ADS_1.ADS1115(address=0x49, i2c=i2c)

channels_1 = [AnalogIn(adc_1,ADS_1.P0),AnalogIn(adc_1,ADS_1.P1),
AnalogIn(adc_1,ADS_1.P2),AnalogIn(adc_1,ADS_1.P3)]

# ADS7830 INITIALISATION
# deflected and reference beam readings

adc_2 = ADS_2.ADS7830(i2c)
REF = 4.2

# BME280 INITIALISATION
bme_count = 4
bmes = [adafruit_bme280.Adafruit_BME280_I2C(mux[i], 0x76) for i in range(bme_count)]

# DS18B20 INITILISATION
out_temp_sensors = DS18B20.get_all_sensors()

# Script start...
duration = 60

out_file = open('data/test.txt','w')
string = """t(s) T1_{ext} T2_{ext} T3_{ext} T4_{ext} 
T1 T2 T3 T4 P1 P2 P3 P4 H1 H2 H3 H4
Turb1_{180} Turb2_{180} Turb3_{180} Turb4_{180}
Turb1_{135} Turb2_{135} Turb3_{135} Turb4_{135}
Turb1_{ref} Turb2_{ref} Turb3_{ref} Turb4_{ref}"""
split = string.split()
title = ','.join(split)
out_file.write(title + '\n')

# Prepare data storage for plotting
max_points = 200  # Maximum number of points to display on the plot
times = []
# create empty lists to store lists of points to plot against time
temperatures = [[] for _ in range(4)]
turbidities = [[] for _ in range(4)]  

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

live_temps = [ax1.plot([], [], label=f'Temperature {i+1}')[0] for i in range(4)]
live_growth = [ax2.plot([], [], label=f'Turbidity {i+1}')[0] for i in range(4)]

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Temperature (°C)')
ax1.tick_params(axis='y', labelcolor='r')

ax2.set_ylabel('Turbidity Growth (V)')
ax1.tick_params(axis='y', labelcolor='b')

plt.title('Real-time Temperature & Turbidity Data')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Function to update the plot
def update_plot():
    for i, line in enumerate(live_temps):
        line.set_data(times, temperatures[i])
        
    for i, line in enumerate(live_growth):
        line.set_data(times, turbidities[i])
    
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    
with tqdm(total=duration, desc="Processing: ") as pbar:
    start = time.time()
    
    while True:
    # evaluating elapsed time at loop start effectively shifts timings by ~3s
    # this sets the time-scale at regular integer stesps
        current = time.time()
        elapsed = current - start
        if elapsed > (duration+1):
            print('Data recordng complete. Terminating...')
            pbar.update(duration - pbar.n)
            IO.cleanup()
            break
        else:
            pbar.update(elapsed - pbar.n)
        # turn on IR LEDs - sleep(2) to let signal settle
            IO.output(LED_Pin, 1)
            start_loop = time.time()
            time.sleep(2)
            
            out_temps = []
            for sensor in out_temp_sensors:
                out_temps.append(sensor.get_temperature())
        # take other readings after DS18B20 - slowest method bottlenecks
            T_s = [bme.temperature for bme in bmes]
            P_s = [bme.pressure for bme in bmes]
            H_s = [bme.humidity for bme in bmes]
            TPH = T_s + P_s + H_s
            voltages_1 = [ch.voltage for ch in channels_1]
            
            channels_2 = [adc_2.read(i) for i in range(8)]
            voltages_2 = [((ch / 65535.0) * REF) for ch in channels_2]
            
            line = f"""{round(elapsed,3)},{",".join(map(str,out_temps))},{",".join(map(str,TPH))},
            {",".join(map(str,voltages_1))},{",".join(map(str,voltages_2))}"""
            end_loop = time.time()
        # turn off IR LEDs
            IO.output(LED_Pin, 0)
            diff = end_loop - start_loop
            dt = max(np.ceil(diff),diff) - diff
            pausing = dt + diff
            out_file.write(line + '\n')
        # Update plot data
            times.append(elapsed)
            for i, temp in enumerate(T_s):
                temperatures[i].append(temp)
            for i, turb in enumerate(voltages_1):
                turbidities[i].append(turb)
            
        # Keep only the last max_points
            if len(times) > max_points:
                times = times[-max_points:]
                for i in range(4):
                    temperatures[i] = temperatures[i][-max_points:]
                    turbidities[i] = turbidities[i][-max_points:]
            
        # Update the plot
            update_plot()
            
        # sets interval between measurements to 30s
            time.sleep(10 - pausing + dt)
    pbar.close()
out_file.close()
