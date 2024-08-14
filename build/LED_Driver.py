import RPi.GPIO as IO  # Import the RPi.GPIO module as IO for GPIO pin control
import time

# Setup GPIO
# for BOARD mode use actual pin number (1-40)
# for BCM mode use GPIO pin number

IO.setmode(IO.BOARD)             # Set mode to BOARD numbering
LED_Pin = 35                     # Define the GPIO pin number for the LED

# Setup LED pin
IO.setup(LED_Pin, IO.OUT)        # Set the LED_Pin as an output pin

try:
    while True:
        IO.output(LED_Pin, 1)
        time.sleep(10)           # Keep the LED on for 10 seconds
        IO.output(LED_Pin, 0)
        time.sleep(10)           # Keep the LED off for 10 seconds
        
except KeyboardInterrupt:
    IO.output(LED_Pin, 0)        # turn the LED off
    IO.cleanup()                 # Clean up the GPIO settings
    pass
