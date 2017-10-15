# Floor Code

## Overview

The code in this directory controls all the lights on the floor as well as reads the weight data sent by the floor.

This code is intended to run on a Raspberry Pi with a special communication sheild that facilitates communication with the floor.  It is started via:
```bash
  python run-show.py
```
For development and testing, use the devserver driver. It allows you to run the code and preview a mock dance floor in a web browser.  It can be run via:
```bash
  python run-show.py --driver devserver
```

## Files/Directories

* **bin** - General executables
* **controller** - The main class, acts a framework for controllers and drivers
* **driver** - Different I/O drivers.  Currently they are `raspberry` for running on a Raspberry Pi and interfacing with its hardware, 'devserver' for development or `opc` (deprecated) for connecting to an existing Open GL server (`gl_server`) that simulates the floor.
* **opc-layouts** - Different OPC pixel layout files when using the opc driver.  These are used by `gl_server` to draw a representation of the floor.
* **processor** - Each file here generates different pixel patterns
* **run-show.py** - The main program that drives the dancefloor

## Setup

1. Clone this repository
```bash
git clone https://github.com/garthwebb/dance-floor.git
```

2. [OPTIONAL] If you will run the code on a RaspberryPi, an SPI library is needed.  If running in dev/virtual mode, SPI is not necessary.
```bash
git clone git://github.com/doceme/py-spidev
sudo apt-get install python-dev
cd py-spidev
sudo make install
```

3. [OPTIONAL] Also needed if running code on a RaspberryPi is the serial module:
```bash
sudo apt-get install python-serial
```

4. [Linux Only] Make sure `pip` is installed:
```bash
sudo apt-get install python-pip
```

5. Install simple websocket server and Flask
```bash
sudo pip install git+https://github.com/dpallot/simple-websocket-server.git
sudo pip install virtualenv
sudo pip install Flask
```

## Running the code

Don't have a light up dance floor?  No problem!  You can see a visualization of the dance floor by running devserver.

1. Start the devserver:
```bash
cd floor
python run-show.py --driver devserver
```
2. Open two browser windows. The dance floor renders at this address:
   http://localhost:1979/

3. The controller renders here:
   http://0.0.0.0:1977/


## Writing a new processor

Different processors provide different ways to drive the floor LEDs. See README.md in the [processor folder](https://github.com/garthwebb/dance-floor/tree/master/floor/processor) for how to write a new processor.
