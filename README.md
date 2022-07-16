# renogymodbus

This package is intended to help you communicate with a Renogy charge controller. It has been tested with a Renogy Rover Elite but should work with other Renogy devices.

## Features
* Read real time data
* Automatic retries

## Connecting to the charge controller
Please check whether your charge controller has a rs232 or rs485 port.

### rs485
Voucher code for 7% off Renogy: https://go.referralcandy.com/share/672HVC9

* rs485 to USB serial cable (UK) https://uk.renogy.com/rs485-to-usb-serial-cable/
* rs485 to USB serial cable (US) https://renogy.com/rs485-to-usb-serial-cable/

<img width="693" alt="image" src="https://user-images.githubusercontent.com/613642/179362448-12a805d1-4475-45cc-b3d7-c8a8e9c4b409.png">

### rs232
Unfortunately the rs232 to USB serial cable has been discontinued by Renogy. It is possible to make your own.

<img width="690" alt="image" src="https://user-images.githubusercontent.com/613642/179362464-35bde1f8-fcb2-43d8-8a52-0232ffa210e8.png">


## Installing the package


To install the package run

```sh
pip install renogymodbus
```

This package requires Python 3, depending on your setup you might have to instead run:

```sh
pip3 install renogymodbus
```


## Command line utility

To run the command line utility and see the debug output run the following on the command line:

```sh
renogymodbus --portname /dev/ttyUSB0 --slaveaddress 1
```

```sh
usage: renogymodbus [-h] [--portname PORTNAME] [--slaveaddress SLAVEADDRESS]

optional arguments:
  -h, --help            show this help message and exit
  --portname PORTNAME   Port name for example /dev/ttyUSB0
  --slaveaddress SLAVEADDRESS
                        Slave address 1-247
```

Example output

```sh
```

## Python usage

To use the library within your Python code

```python
from renogymodbus.driver import RenogyChargeController

controller = RenogyChargeController("/dev/ttyUSB0", 1)
controller.get_solar_voltage()
```

See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/driver.py for all available methods
