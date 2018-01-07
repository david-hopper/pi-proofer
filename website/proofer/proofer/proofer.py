import os
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from fileLock import FileLock

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
	DATABASE=os.path.join('/home/pi/pi-proofer/status.json'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='password'
	))
app.config.from_envvar('PROOFER_SETTINGS', silent=True)

def read_db():
	"""Connects to the JSON database and returns a dict"""
	with FileLock(app.config['DATABASE'], delay=0.05):
		with open(app.config['DATABASE'], 'r') as f:
			db = json.loads(f.read())
	return db

def write_db(db):
	"""Connects and writes to the JSON database"""
	with FileLock(app.config['DATABASE'], delay=0.05):
		with open(app.config['DATABASE'], 'w') as f:
			f.write(json.dumps(db, indent=4))

def init_db():
	"""Create the data base"""
	db = {"running" : 0, "set_point": 80, 
		  "set_range" : 1,
		  "time_array": [], 
		  "temp_array": [],
		  "set_point_array" : [],
		  "actual_temp" : [],
		  "actual_temp" : []
		  }
	write_db(db)
	

@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database."""
	init_db()
	print("Initialized the database.")

@app.route('/', methods=['GET', 'POST'])
def show_status():
	db = read_db()
	return render_template('test.html', db=db)

@app.route('/_status', methods=['GET'])
def status():
	db = read_db()
	return jsonify(db)

@app.route('/update_props', methods=['POST'])
def update_status():
	set_point = request.form['set_point']
	set_range = request.form['set_range']

	db = read_db()
	db['set_point'] = float(set_point)
	db['set_range'] = float(set_range)

	write_db(db)

	print("The set point was " + set_point)
	print("The range was " + set_range)
	return redirect('/')

@app.route('/update_run_status', methods=['POST'])
def update_run_status():

	db = read_db()
	if 'start_button' in request.form.keys() :
		running = 1
	elif 'stop_button' in request.form.keys() :
		running = 0
	else :
		running = db['running']

	db['running'] = running
	write_db(db)

	return redirect('/')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
