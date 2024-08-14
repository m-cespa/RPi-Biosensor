import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time                            #calling time to provide delays in program

IO.setmode(IO.BOARD)
Fan_Pin = 35
IO.setup(Fan_Pin,IO.OUT)
p = IO.PWM(Fan_Pin,1000)
p.start(0)
p.ChangeDutyCycle(15)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    p.stop(0)
    IO.cleanup()
    pass
