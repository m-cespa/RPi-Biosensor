import RPi.GPIO as IO
import time

class LED_IO:
    """"""
    def __init__(self, pin: int, board_mode: str):
        """GPIO operated LED class with simple top_hat and finish methods"""
        self.pin = pin
        self.board_mode = board_mode.upper()
        if self.board_mode == 'BOARD':
            IO.setmode(IO.BOARD)
        elif self.board_mode == 'BCM':
            IO.setmode(IO.BCM)
        IO.setup(self.pin, IO.out)
        IO.output(self.pin, 0)

    def top_hat(self, duration: float):
        IO.output(self.pin, 1)
        time.sleep(duration)
        IO.output(self.pin, 0)

    def finish(self):
        IO.output(self.pin, 0)
        IO.cleanup()
