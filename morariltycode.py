

from threading import Thread
from pvcheetah import *
from pvrecorder import PvRecorder

import board
import busio
import digitalio
import time
import serial
import adafruit_thermal_printer
import pygame
import os
from adafruit_mcp230xx.mcp23017 import MCP23017



uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.19)
printer = ThermalPrinter(uart)
printer.warm_up()
printer.print("System loading...")
printer.feed(4)
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
LED1 = mcp.get_pin(0)
LED1.switch_to_output(value=False)
LED2 = mcp.get_pin(2)
LED2.switch_to_output(value=False)
SW1 = mcp.get_pin(4)
SW1.direction = digitalio.Direction.INPUT
SW1.pull = digitalio.Pull.UP
printer.print("System Ready")
printer.feed(4)



class Demo(Thread):
	def __init__(
			self,
			access_key: str,
			model_path: Optional[str],
			library_path: Optional[str],
			endpoint_duration_sec: float,
			enable_automatic_punctuation: bool):
		super(Demo, self).__init__()

		self._access_key = access_key
		self._model_path = model_path
		self._library_path = library_path
		self._endpoint_duration_sec = endpoint_duration_sec
		self._enable_automatic_punctuation = enable_automatic_punctuation
		self._is_recording = False
		self._stop = False

		
	def run(self):
		self._is_recording = True

		o = None
		recorder = None

		try:
			o = create(
				access_key=self._access_key,
				library_path=self._library_path,
				model_path=self._model_path,
				endpoint_duration_sec=self._endpoint_duration_sec)
			recorder = PvRecorder(device_index=-1, frame_length=o.frame_length)
			recorder.start()

			print('Cheetah version : %s' % o.version)

			curse_list = ['bullshit', 'bullshitting', 'dipshit', 'horseshit', 'shit', 'shithead', 'shitty', 'fuck', 'fucks', 'fucked', 'fucked-up', 'fucker', 'fuckers', 'fucking', 'fucks', 'ass', 'asses', 'big-ass', 'dumb-ass', 'dumbass', 'asshole', 'bastard', 'bitch', 'bitches', 'bitchiness', 'bitching', 'bitchy', 'piss', 'pissed', 'cunt', 'dick', 'dicks', 'dickhead']

			while True:
				partial_transcript, is_endpoint = o.process(recorder.read())
				if SW1.value == False:
					morality()
				# print(partial_transcript, end='', flush=True)
				for word in curse_list:
					if word in partial_transcript:
						print("curse detected: " + word)
						morality()
				#if is_endpoint:
					#for word in curse_list:
						#if word in str(o.flush()):
							#print("curse detected: " + word)
							#morality()
					# print(o.flush())
		except KeyboardInterrupt:
			pass
		finally:
			if recorder is not None:
				recorder.stop()

			if o is not None:
				o.delete()

def morality():

	LED1.value = True
	LED2.value = True

	pygame.mixer.init()
	pygame.mixer.music.load("<path to mp3>/violation.mp3")
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		pass

	printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
	printer.inverse = True
	printer.print("  MORALITY  ")
	printer.inverse = False
	printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT

	printer.bold = True
	printer.print("NAME: Irish Demon")
	printer.print("ADDRESS: Cork, Ireland")
	printer.print("SECTOR: South East")
	printer.print("STATUS: Level #3")
	printer.print("VIOLATION: Verbal morality")
	printer.print("PUNISHMENT: Fine")
	printer.print("FINE: 1 Credit")
	printer.print("ADVISORY: ")
	printer.bold = False
	printer.print("To avoid future morality")
	printer.print("violation fines, please")
	printer.print("behave in a socially")
	printer.print("acceptable way")
	printer.bold = True
	printer.print("Be well")
	printer.bold = False
	printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
	printer.inverse = True
	printer.print("  VIOLATION  ")
	printer.inverse = False
	printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
	printer.feed(5)

	LED1.value = False
	LED2.value = False



def main():
	
	my_access_key = '<your api key>'
	my_model_path = '/home/<path to your model>/curse_detector--cheetah-v1.1.0--22-10-28--21-51-17.pv'

	Demo(
		access_key=my_access_key,
		library_path=None,
		model_path=my_model_path,
		endpoint_duration_sec=float(1.0),
		enable_automatic_punctuation=not 'store_true').run()


if __name__ == '__main__':
	main()