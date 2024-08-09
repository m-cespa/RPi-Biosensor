import RPi.GPIO as IO  # Import the RPi.GPIO module as IO for GPIO pin control
import time  # Import the time module to provide delays in the program

# Setup GPIO
IO.setmode(IO.BOARD)  # Set the GPIO mode to BOARD numbering
LED_Pin = 35  # Define the GPIO pin number for the LED

# Setup LED pin
IO.setup(LED_Pin, IO.OUT)  # Set the LED_Pin as an output pin
p = IO.PWM(LED_Pin, 5000)  # Initialize PWM on LED_Pin with a frequency of 5000 Hz (5 kHz)
p.start(0)  # Start PWM with a duty cycle of 0%

try:
    while True:
        p.ChangeDutyCycle(100)  # Set the duty cycle to 100% to turn the LED on
        time.sleep(10)  # Keep the LED on for 10 seconds
        p.ChangeDutyCycle(0)  # Set the duty cycle to 0% to turn the LED off
        time.sleep(20)  # Keep the LED off for 20 seconds

except KeyboardInterrupt:
    p.stop()  # Stop the PWM signal
    IO.cleanup()  # Clean up the GPIO settings
    pass
