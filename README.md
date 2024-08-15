# Python Package Installation:

(python packages were all installed to a virtual environment, see [1](https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi/overview) for documentation)

create a python virtual environment:
```
sudo apt install python3-venv
python3 -m venv <insert desired environment name>
```

activate your virtual environment: (here it is called 'venv')
```
source venv/bin/activate
```
once activated:
```
pip3 install adafruit-python-shell, ds18b20
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```
system will now ask to reboot, after reboot and activation of venv:
```
pip3 install adafruit-circuitpython-ads1x15 adafruit-circuitpython-ads7830 adafruit-circuitpython-tca9548a adafruit-circuitpython-bme280
```
if `board` module is causing issues, try:
```
python3 -m pip install --upgrade --force-reinstall adafruit-blinka
```

# Method: (for RPI Model 3B+)

(for circuit information refer to schematic diagram [here](./docs/labelled_schematic.png))

**PCA9546** (4 Channel Multiplexer):\
The multiplexer was used to connect 4 BME280's onto 1 rpi. The multiplexer's package `adafruit-circuitpython-tca9548a` was installed to initialise multiple same address i2c device access [2](https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/circuitpython-python). The `mux` object seen in the script allowes accesss to the devices connected to each of the multiplexer's 4 channels by specifying the device's multiplexer channel connection (index of the mux object) and i2c address. The PCA9546's specifications can be found here [3](https://www.adafruit.com/product/5663).


**BME280** (Pressure, Temperature, Humidity):\
The sensor's adafruit package `adafruit-circuitpython-bme280` was installed to access the sensor class' methods [4](https://pypi.org/project/adafruit-circuitpython-bme280/). The adafruit package was used rather than the standard `bme280` package as creating instances of the `BME280` class in the adafruit package automates calibration which was convenient given multiple instances were called. If using a single BME280, it can be initialised in the script following the steps given by the `bme280` package's repository [5](https://pypi.org/project/RPi.bme280/). The `smbus2` package [6](https://pypi.org/project/smbus2/) did not need to be installed for our configuration using the multiplexer and `adafruit-circuitpython-bme280` package (for the `smbus2` method, refer to [7](https://randomnerdtutorials.com/raspberry-pi-bme280-python/)). For our purposes, the i2c initialisation steps were done for the multiplexer, and for each of the 4 entires in `mux`, the `0x76` i2c address (the BME280) was specified. Each BME280 was connected to a pair of clock (SCL) and data (SDA) pins on the multiplexer. The BME280's specifications can be found here [8](https://thepihut.com/products/bme280-environmental-sensor#:~:text=A%20tiny%20sensor%20breakout%20with,3.3V%2F5V%20voltage%20levels.).


**DS18B20** (1-Wire Temperature):\
The sensor was wired to the rpi following the steps given by [9](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/). The sensor's package `ds18b20` was used rather than the method outlined in [10](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/). The `ds18b20` package was setup following the steps given in the package's github repository [11](https://github.com/rgbkrk/ds18b20). The DS18B20's specifications can be found here [12](https://thepihut.com/products/ds18b20-one-wire-digital-temperature-sensor).


**ADS1115 & ADS7830** (4-channel * 8-channel Analogue-Digital Converters):\
The sensors were daisy chained and then connected across the same SCL/SDA pins as the PCA9546. The two devices have different addresses to each other and to the PCA9546 (`0x70` for PCA9546, `0x49` for ADS1115, `0x48` for ADS7830) and can be recognised as different inputs along the same i2c pins. To check that both multiplexer (mux) and analogue-digital converters (adc) are being read by the rpi, type `sudo i2cdetect -y 1` into the terminal and the above addresses should appear. The i2c address of the ADS1115 can be altered by connecting the ADDR pin to one of GND, VIN, SDA, SCL which will change the device address to `0x48`, `0x49`, `0x4a`, `0x4b` accordingly. A similar procedure can be done for the ADS7830 [13](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ads7830-8-channel-8-bit-adc.pdf) but for the circuit here described, the default `0x48` address was opted for.

The following lines were passed into terminal (order specific) to install the `ads1x15` (ADS1115) library:
1. `pip3 install --upgrade adafruit-python-shell`
2. `wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py`
3. `python3 raspi-blinka.py`
4. `pip3 install adafruit-circuitpython-ads1x15`\

Installation of the `ads7830` library after the above steps proved simpler now that the Adafruit_Blinka library was present. The following line was passed into terminal:
`pip3 install adafruit-circuitpython-ads7830` [14](https://learn.adafruit.com/adafruit-ads7830-8-channel-8-bit-adc/circuitpython-and-python)

{NOTE: you must not pass `pip3 install board` into terminal as this `board` module is completely separate from the `adafruit-circuitpython` library and will cause conflict, the correct package is installed via `raspi.blinka`. Concurrent explicit installation of the package can cause package failure. Further documentation on installing the `adafruit` and `blinka` packages necessary for the ADS1115 can be found here [15](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi). If there is an issue with `board` attempt force reinstalling Blinka with `python3 -m pip install --upgrade --force-reinstall adafruit-blinka`}

The `busio` package was also installed. Either the `busio` or `board` packages can be used to initialise i2c bus connections. The `busio` package allows for explicit intialisation of an i2c connection where the clock and data i2c pins can be specified (if a non default i2c bus is being used). The `board` package's `I2C()` method (`i2c_init = board.I2C()`) on the other hand will initialise the i2c bus using the standard clock and data pins. To enable future intialisation of non-default i2c buses, the `busio` initialisation (which still requires the `board` package) was chosen.

When creating the `ADS1115` & `ADS7830` objects, the same `i2c` argument as for the PCA9546 was passed whilst the i2c address was altered as required to specify each device. The ADS1115 was initialised in the script following the steps given by [16](https://www.instructables.com/How-to-Use-ADS1115-With-the-Raspberry-Pi-Part-1/). To avoid conflict between the `ADS1115` and `ADS7830` classes, their methods are inherently different. The `ADS7830` class allows only direct reading of the 32-bit signal which requires manual conversion to a voltage value - refer to [17](https://learn.adafruit.com/adafruit-ads7830-8-channel-8-bit-adc/circuitpython-and-python).

The ADS1115's specifications can be found here [18](https://thepihut.com/products/adafruit-ads1115-16-bit-adc-4-channel-with-programmable-gain-amplifier). The ADS7830's specifications can be found here [19](https://thepihut.com/products/adafruit-ads7830-8-channel-8-bit-adc-with-i2c-stemma-qt-qwiic).

**IR EMITTER-RECEIVER**:\
To yield a proxy measurement of solution turbidity, a pair of IR emitter and IR Photodiode were used. The WL-TIRC THT Infrared Round Waterclear was selected as an emitter (datasheet: [20](https://docs.rs-online.com/c30e/A700000007241424.pdf)) and the IR T-1 3/4 PIN Silicon Photodiode as a receiver (datasheet: [21](https://docs.rs-online.com/461d/0900766b808b25c5.pdf)), to note: the photodiode is opaque to visible light. Photodiodes were positioned at 180° and 90° (and a reference photodiode for each LED to check whether it was on) on the opposing side of the reactor beakers to measure through and deflected beams accordingly. To measure only the change in voltage across the photodiodes, an op-amp differential amplifier circuit was trialled where one photodiode would be in an isolated environment and the other exposed to IR. Due to variations in the base resistances of the photodiodes, wires and resistors, this configuration resulted in non-zero base reading output and was hence not used.


**PWM STIRRER**:\
Cooling fans with magnets were used to drive magnetic stirrer beads in each reactor beaker. The `PWM_Stirrer.py` script was run in the background to `ALL_Sensors.py` to keep the stirrers rotating at a prescribed fixed velocity modulated by using Pulse Wave Modulation (PWM) through a GPIO pin. The script uses the `RPi.GPIO` package which should be pre-installed on updated versions of Raspbian - to check this refer to [22](https://sourceforge.net/p/raspberry-gpio-python/wiki/install/).
