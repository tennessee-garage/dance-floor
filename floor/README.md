# Floor Code

[![Build Status](https://travis-ci.org/tennessee-garage/dance-floor.svg?branch=master)](https://travis-ci.org/tennessee-garage/dance-floor)

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

### Prerequisites

You'll need `poetry`. On a Mac with Homebrew, install with:

```
$ brew install poetry
```

For other options, see [the Poetry installation docs](https://python-poetry.org/docs/#installation).

### Developer setup

Install dependencies - one time, and whenever you change them:
```
$ poetry install
```

Then do all work within a poetry shell:
```
$ poetry shell
$ python ...
```

To run tests:

```
$ pytest
```

It is recommend you install `pre-commit` to take care of auto-formatting code.
```
$ brew install pre-commit
$ pre-commit install
```

### Production setup (Raspberry Pi)


1. Clone this repository
```bash
git clone git@github.com:tennessee-garage/dance-floor.git
```

2. [OPTIONAL] If you will run the code on a RaspberryPi, an SPI library is needed.  If running in dev/virtual mode, SPI is not necessary.
```bash
git clone git@github.com:doceme/py-spidev.git
sudo apt-get install python-dev
cd py-spidev
sudo make install
```

3. Install poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. Install depencencies (from within the dance-floor repository)
```bash
cd floor
poetry install
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
