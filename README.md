# renogymodbus

This package is intended to help you communicate with a Renogy charge controller. It has been tested with a Renogy Rover Elite but should work with other Renogy devices.

## Features
* Read real time data
* Automatic retries

## Connecting to the charge controller or battery
This library has been tested with the following devices:
* Renogy Rover Elite 20A MPPT Solar Charge Controller
* Renogy 12V 100Ah Smart Lithium Iron Phosphate Battery

The library should work with other Renogy devices, please raise an issue if you have problems or have tested that the library works with your device.

Please check whether your charge controller or battery has a rs232 or rs485 port.

### rs485
Voucher code for 7% off Renogy: http://73renogy.refr.cc/rosswarren

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
usage: renogymodbus [-h] [--portname PORTNAME] [--slaveaddress SLAVEADDRESS]
                   [--device {charge_controller,smart_battery}]
                   [--find-slave-address]

optional arguments:
  -h, --help            show this help message and exit
  --portname PORTNAME   Port name for example /dev/ttyUSB0
  --slaveaddress SLAVEADDRESS
                        Slave address 1-247
  --device {charge_controller,smart_battery}
                        Device to read data from. Either charge_controller or
                        smart_battery
  --find-slave-address  Find slave address of modbus device
```

Example commands:
```sh
renogymodbus --device smart_battery --portname /dev/ttyUSB0 --slaveaddress 48
```

```sh
renogymodbus --device charge_controller --portname /dev/ttyUSB0 --slaveaddress 1
```

```sh
renogymodbus --find-slave-address --portname /dev/ttyUSB0
```

Example output for charge controller (ML2420 in this case).
Run from git sandbox.
```sh
renogymodbus$ python3 -m renogymodbus.command_line
Real Time Charge Controller Data : ML2420
Controller SW version: V4.4.2
Controller HW version: V0.0.3
Controller serial number: #3 date code 0-3
Controller temperature: 26 °C
Solar voltage: 26.0 V
Solar current: 0.46 A
Solar power  : 12 W
Solar power today, max: 18 W
Solar power today, min: 0 W
Load voltage: 0.0 V
Load current: 0.0 A
Load power  : 0 W
Battery voltage: 13.8 V
Battery voltage today, max: 14.4 V
Battery voltage today, min: 13.0 V
Battery state of charge: 100 %
Battery temperature: 25 °C
Maximum charging current today : 1.37 A
Charging today : 12 Ah
Battery max discharge current: 0.0 A
Battery max discharge power: 0 A
Discharging today : 0 Ah
```

Example output for smart battery
```
Real Time Smart Battery Data
Cell voltages: [3.3, 3.3, 3.3, 3.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]V
Cell temperatures: [24.0, 24.0, 24.0, 24.0, 1835.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]°C
BMS temperature: 0.0°C
Environment temperatures: [25.0, 25.0]°C
Heater temperatures: [25.0, 25.0]°C
Current: -0.2A
Voltage: 13.3V
Remaining capacity: 98.966Ah
Total capacity: 100.0Ah
State of charge: 98.966%
Cycle number: 0
Charge voltage limit: 14.8V
Discharge voltage limit: 10.0V
Charge current limit: 50.0A
Discharge current limit: -100.0A
```

## Python usage

To use the library within your Python code

### Charge Controller

```python
from renogymodbus import RenogyChargeController

controller = RenogyChargeController("/dev/ttyUSB0", 1)
controller.get_solar_voltage()
```

See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/charge_controller.py for all available methods

### Smart Battery

```python
from renogymodbus import RenogySmartBattery

battery = RenogySmartBattery("/dev/ttyUSB0", 48)
battery.get_voltage()
```
See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/smart_battery.py for all available methods

# On Rover Modbus registers

See https://www.going-flying.com/blog/files/141/ROVER_MODBUS.pdf
