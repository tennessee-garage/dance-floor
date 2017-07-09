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

1. Clone the OpenPixelControl repository:
```bash
git clone https://github.com/zestyping/openpixelcontrol.git
```
or use JB's fork, where lights are rendered as squares instead of points:
```bash
https://github.com/jbrecht/openpixelcontrol.git
```
2. Clone this repository
```bash
git clone https://github.com/garthwebb/dance-floor.git
```
## Running the code

Don't have a light up dance floor?  No problem!  You can see a visualization of the dance floor by running the `gl_server` provided by OpenPixelControl.

1. Start the `gl_server` with the dance floor layout:
```bash
# Replace $OPC_PATH with whereever you installed OpenPixelControl
# and $DANCE_PATH with wherever this repo exists
$OPC_PATH/bin/gl_server -l $DANCE_PATH/floor/opc-layouts/simple-dance-floor.json
```
2. Next start the show code:
```bash
python run-show.py --driver opc --processor raver_plaid
```

## Writing a new processor

Different processors provide different ways to drive the floor LEDs. See README.md in the [processor folder](https://github.com/garthwebb/dance-floor/tree/master/floor/processor) for how to write a new processor.
