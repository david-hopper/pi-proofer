import os
import json
import time
import datetime
import ds18b20 as temp
import RPi.GPIO as GPIO

from fileLock import FileLock

curr_dir = os.getcwd()

db_file = curr_dir[0:-10] + 'status.json'

output_type =  GPIO.BOARD
output_chan = 13
def read_db():
	"""Connects to the JSON database and returns a dict"""
	with FileLock(db_file, delay=0.05):
		with open(db_file, 'r') as f:
			db = json.loads(f.read())
	return db

def write_db(db):
	"""Connects and writes to the JSON database"""
	with FileLock(db_file, delay=0.05):
		with open(db_file, 'w') as f:
			f.write(json.dumps(db, indent=4))

# set wait times
loop_pause = 5
record_pause = 30
write_pause = record_pause
counter = 1
timing = {'loop_start' : time.time(),
	'record_start' : time.time(),
	'write_start' : time.time()}
# Clear the temperature buffer
curr_temp = temp.read_temp()
GPIO.setmode(output_type)
GPIO.setup(output_chan, GPIO.OUT)

while True:
	time.sleep(loop_pause)
	db = read_db()
	if db['running'] == 1 : 

		print('Checking temperature...')
		curr_temp = temp.read_temp()
		
		lower = curr_temp < db['set_point'] - db['set_range']
		exceed = curr_temp > db['set_point'] + db['set_range']
		if lower :
			GPIO.output(output_chan, 1)
		elif exceed:
			GPIO.output(output_chan, 0)

		print(curr_temp)

		if time.time() - timing['record_start'] > record_pause :
			db['actual_temp'] = curr_temp
			db['temp_array'].append(curr_temp)
			db['set_point_array'].append(db['set_point'])
			db['time_array'].append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		if time.time() - timing['write_start'] > write_pause :
			write_db(db)

		counter = 1
	else:
		if counter == 1 :
			GPIO.output(output_chan, 0)
			counter = counter + 1








