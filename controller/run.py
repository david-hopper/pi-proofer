import os
import json
import time
import datetime
import ds18b20 as temp

from fileLock import FileLock

curr_dir = os.getcwd()

db_file = curr_dir[0:-10] + 'status.json'

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
loop_pause = 1.5
record_pause = 2
write_pause = 4

timing = {'loop_start' : time.time(),
	'record_start' : time.time(),
	'write_start' : time.time()}


while True:
	time.sleep(loop_pause)
	db = read_db()
	if db['running'] == 1 : 

		print('Checking temperature...')
		curr_temp = temp.read_temp()
		
		print(curr_temp)

		if time.time() - timing['record_start'] > record_pause :
			db['actual_temp'] = curr_temp
			db['temp_array'].append(curr_temp)
			db['set_point_array'].append(db['set_point'])
			db['time_array'].append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		if time.time() - timing['write_start'] > write_pause :
			write_db(db)






