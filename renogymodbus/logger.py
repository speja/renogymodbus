import argparse
import datetime, time
import json
from renogymodbus import RenogyChargeController

if __name__ == "__main__":
    while True:
        try:
            cc = RenogyChargeController('/dev/ttyUSB0', 1)
            data = dict()
            data['soc'] = cc.battery_state_of_charge
            data['Upv'] = cc.solar_voltage
            data['Ipv'] = cc.solar_current
            data['Ppv'] = cc.solar_power
            data['Ubat'] = cc.battery_voltage
            data['Ubatmax'] = cc.maximum_battery_voltage_today
            data['Ubatmin'] = cc.minimum_battery_voltage_today
            data['ICbatmax'] = cc.max_charging_current
            data['ICbat'] = cc.battery_charge_current
            data['DayCharge'] = cc.charging
            data['DayEnergy'] = cc.power_generation
            data['Tbat'] = cc.battery_temperature
            data['Tctrl'] = cc.controller_temperature
            data['Cstate'] = cc.controller_charging_state
            print(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}: {json.dumps(data)}")
        except Exception as e:
            print(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}: {e}")
        time.sleep(8)

