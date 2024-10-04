# general pwm motor element class
import pigpio

pi = pigpio.pi()

class PWM_Motor:
	def __init__(self, pwm_pin: int, dir_pin: int, freq: int):
		if not pi.connected:
			print('pigpio not running')
			exit()
			
		self.board_mode = board_mode.upper()
		self.pwm_pin = pwm_pin
		self.dir_pin = dir_pin
		self.freq = freq
		
		pi.set_mode(pwm_pin, pigpio.OUTPUT)
		pi.set_mode(dir_pin, pigpio.OUTPUT)
		
		pi.set_PWM_frequency(pwm_pin, freq)
		
	def run(self, power: int, forward: bool):
		"""Basic forward & backard motor functionality"""
		if forward:
			pi.write(self.dir_pin, 1)
		else:
			pi.write(self.dir_pin, 0)
		
		# power arg is 8-bit
		pi.set_PWM_dutycycle(self.pwm_pin, power)
		
	def linear(self, time: float, start_power: float, end_power: float, forward: bool):
		"""Linear increase in motor output over specified time duration"""
		if not forward and end_power > start_power:
			raise ValueError
			
		dt = 0.01
		bins = time / dt
		
		self.run(start_power, forward)
		
		if forward:
			for i in bins:
				pi.set_PWM_dutycycle(self.pwm_pin, start_power + i*(end_power-start_power))
				time.sleep(dt)
		else:
			for i in bins:
				pi.set_PWM_dutycycle(self.pwm_pin, start_power - i*(end_power-start_power))
				time.sleep(dt)
		
	def stop():
		pi.set_PWM_dutycycle(self.pwm_pin, 0)
		
peltier = PWM_Motor(24, 25, 100)

peltier.run(100, forward=True)

			
