# pi-proofer
Control a proofing chamber through a local network on a raspberry pi.



## Hardware Requirements
* Raspberry Pi with Raspian OS
* Relay board (see [IoT Relay Board](https://www.amazon.com/Iot-Relay-Enclosed-High-power-Raspberry/dp/B00WV7GMA2) )
* DS18B20 temperature sensor ([link](https://www.amazon.com/Gikfun-DS18B20-Temperature-Waterproof-EK1083x3/dp/B00Q9YBIJI/ref=sr_1_1?s=electronics&ie=UTF8&qid=1515352720&sr=1-1&keywords=ds18b20))
* 4.7k pull up resistor (see Adafruit [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware) for hook up)
* Box to hold dough and maintain temperature
* 40-60 W incandescent bulb

## External Software Requirements
* [flask](http://flask.pocoo.org/docs/0.12/)

## Quick Guide
Hook up the relay switch to the GPIO pin 13 (GPIO27 label).

Assign a static local IP address to your raspberry pi, this will allow you to access the web interface from the same address.

Install flask for python 3
```
pip3 install flask
```

Clone the repository to the pi user's home directory (~/)
```
git clone https://github.com/david-hopper/pi-proofer.git
```

Add the following statements to the ~/.profile file to serve the website and start the controller upon login. This simplifies the turn on procedure to simply plugging in the raspbery pi and relay.

To edit the .profile file, enter
```
pi@raspberrypi:~/nano .profile
```

Then add
```
# Change into proofer
cd "pi-proofer/"

# Force clear the lock file if it wasn't cleaned up
rm -f "status.json.lock"

# Run the website and controller in two different tmux windows and auto detach
tmux new -d -s "website" ". ./run_website"
tmux new -d -s "controller" ". ./run_controller"
```

and save the file

Reboot the raspberry pi and it will be ready to go. Access your pi by entering <ipaddress>:5000 into a browser on the same wifi network as the raspberyy pi.

## Notes
To access the two processes running on the raspberry pi, one can enter
```
tmux attach 'website'
```
or 
```
tmux attach 'controller'
```

To view the website or controller outputs

