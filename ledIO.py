import RPi.GPIO as IO
import time

bcm = {7:4, 11:17, 12:18, 13:27, 15:22, 16:23, 18:24, 22:25, 
    29:5, 31:6, 32:12, 33:13, 35:19, 36:16, 37:26, 38:20, 40:21}

class LED_IO:
    def __init__(self, board_mode:str, pin:int):
        """GPIO operated LED class with simple top_hat and finish methods"""
        self.board_mode = board_mode.upper()
        self.pin = pin
        if self.board_mode == 'BOARD':
            IO.setmode(IO.BOARD)
        elif self.board_mode == 'BCM':
            self.pin = bcm[self.pin]
            IO.setmode(IO.BCM)
        else:
            raise ValueError("Invalid board mode: use 'BCM' or 'BOARD'")
        IO.setup(self.pin, IO.OUT)
        IO.output(self.pin, 0)
        

    def top_hat(self, duration: float):
        IO.output(self.pin, 1)
        time.sleep(duration)
        IO.output(self.pin, 0)
        
    def on(self):
        IO.output(self.pin, 1)
        
    def off(self):
        IO.output(self.pin, 0)

    def finish(self):
        IO.output(self.pin, 0)
        IO.cleanup()
        
