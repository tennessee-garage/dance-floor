# Floor Code

## Overview

The code in this directory controls all the lights on the floor as well as reads the weight data sent by the floor.

This code is intended to run on a Raspberry Pi with a special communication sheild that facilitates communication with the floor.  The code is started via:
```bash
  python run-show.py --driver raspberry
```
There is a test mode of this code that allows running and debugging from a computer rather than a Raspberry Pi.  It uses OpenPixelControl talking to an Open GL server (`gl_server`) to simulate the dancefloor   It can be run via:
```bash
  python run-show.py --driver opc
```

## Files/Directories

* **bin** - General executables
* **controller** - The main class, acts a framework for controllers and drivers
* **driver** - Different I/O drivers.  Currently they are `raspberry` for running on a Raspberry Pi and interfacing with its hardware or `opc` for connecting to an existing Open GL server (`gl_server`) that simulates the floor.
* **opc-layouts** - Different OPC pixel layout files.  These are used by `gl_server` to draw a representation of the floor.
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
```

3. Install simple websocket server and Flask
```bash
sudo pip install git+https://github.com/dpallot/simple-websocket-server.git
sudo pip install virtualenv
sudo pip install Flask
```

## Running the code

Don't have a light up dance floor?  No problem!  You can see a visualization of the dance floor by running the `gl_server` provided by OpenPixelControl.

1. Start the devserver:
```bash
cd floor
python run-show.py --driver devserver
```
2. Open two browser windows. The dance floor renders at this address:
   http://localhost:1979/

3. The controller renders here:
   http://0.0.0.0:1977/

## Running with OPC

This is the previous method for testing the dance floor code that used Open Pixel Control as a framework for mocking the floor.  It provides an OpenGL server that can simulate what the floor will look like when data is sent to it.  The web interface is the preferred way to test, so this is here primarly as an FYI.

### Setup

1. If on a linux machine (not necessary on a Mac) install a few required libraries
```bash
sudo apt-get install mesa-common-dev freeglut3-dev
```
2. Build a modified version of the OPC server that includes jbrecht's change to make the LEDs square rather than round:
```bash
cd floor/opc
make
```

### Running

1. Start the `gl_server` with the dance floor layout:
```bash
floor/opc/bin/gl_server -l floor/opc-layouts/simple-dance-floor.json
```
2. Next start the show code:
```bash
python floor/run-show.py --driver opc --processor raver_plaid
```

## Writing a new processor

Different processors provide different ways to drive the floor LEDs. See README.md in the [processor folder](https://github.com/garthwebb/dance-floor/tree/master/floor/processor) for how to write a new processor.
