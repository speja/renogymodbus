import minimalmodbus
import serial

from renogymodbus.retriable_instrument import RetriableInstrument


class RenogyChargeController(RetriableInstrument):
    """Instrument class for Renogy Charge Controllers.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    def __init__(self, portname, slaveaddress):
        super().__init__(portname, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = 1
        self.serial.timeout = 1
        self.mode = minimalmodbus.MODE_RTU

        self.clear_buffers_before_each_transaction = True

    def get_solar_voltage(self):
        """PV array input in volts"""
        return self.retriable_read_register(0x0107, 1, 3, False)

    @property
    def solar_voltage(self):
        """PV array input voltage [V]"""
        return self.get_solar_voltage()
    
    def get_solar_current(self):
        """PV array input in amps"""
        return self.retriable_read_register(0x0108, 2, 3, False)

    @property
    def solar_current(self):
        """PV array input current [A]"""
        return self.get_solar_current()
    
    def get_solar_power(self):
        """PV array input in watts"""
        return self.retriable_read_register(0x0109, 0, 3, False)

    @property
    def solar_power(self):
        """PV array input power [W]"""
        return self.get_solar_power()

    def get_load_voltage(self):
        """Load output in volts"""
        return self.retriable_read_register(0x0104, 1, 3, False)

    @property
    def load_voltage(self):
        """Load output voltage [V]"""
        return self.get_load_voltage()

    def get_load_current(self):
        """Load output in amps"""
        return self.retriable_read_register(0x0105, 2, 3, False)

    @property
    def load_current(self):
        """Load output current [A]"""
        return self.get_load_current()
    
    def get_load_power(self):
        """Load output in watts"""
        return self.retriable_read_register(0x0106, 0, 3, False)

    @property
    def load_power(self):
        """Load output power [W]"""
        return self.get_load_power()
    
    def get_battery_voltage(self):
        """Battery voltage"""
        return self.retriable_read_register(0x0101, 1, 3, False)

    @property
    def battery_voltage(self):
        """Battery voltage [V]"""
        return self.get_battery_voltage()
    
    def get_battery_state_of_charge(self):
        """Battery state of charge [%]"""
        return self.retriable_read_register(0x0100, 0, 3, False)

    @property
    def battery_state_of_charge(self):
        """Battery state of charge"""
        return self.get_battery_state_of_charge()
    
    def get_battery_temperature(self):
        """Battery temperature"""
        register_value = self.retriable_read_register(0x0103, 0, 3, False)
        battery_temperature = register_value & 0b0000000001111111
        battery_temperature_sign = (register_value & 0b0000000010000000) >> 7
        battery_temperature = -battery_temperature if battery_temperature_sign == 1 else battery_temperature
        return battery_temperature

    @property
    def battery_temperature(self):
        """Battery temperature [°C]"""
        return self.get_battery_temperature()

    @property
    def battery_charge_current(self):
        """Charging current of battery"""
        return self.retriable_read_register(0x0102, 2, 3, False)

    def get_controller_temperature(self):
        """Temperature inside equipment"""
        register_value = self.retriable_read_register(0x0103, 0, 3, False)
        controller_temperature = (register_value & 0b0111111100000000) >> 8
        controller_temperature_sign = (register_value & 0b1000000000000000) >> 15
        controller_temperature = -controller_temperature if controller_temperature_sign == 1 else controller_temperature
        return controller_temperature

    @property
    def controller_temperature(self):
        """Controller internal temperature [°C]"""
        return self.get_controller_temperature()

    @property
    def controller_model(self):
        """Read product model"""
        return self.retriable_read_string(0x000C, 8, 3).strip()

    @property
    def controller_software(self):
        """Software version number"""
        # FIXME numbering scheme from ROVER_MODBUS.pdf
        sw = self.retriable_read_registers(0x0014, 2, 3)
        sw = f"V{sw[0]%256}.{sw[1]//256}.{sw[1]%256}"
        return sw

    @property
    def controller_hardware(self):
        """Hardware version model"""
        hw = self.retriable_read_registers(0x0016, 2, 3)
        hw = f"V{hw[0]%256}.{hw[1]//256}.{hw[1]%256}"
        return hw

    @property
    def controller_serial(self):
        """Read controller serial number"""
        # FIXME does not fit the ML2420 mppt regulator
        sn = self.retriable_read_registers(0x0016, 2, 3)
        sn = f"#{sn[1]} date code {sn[1]//256}-{sn[1]%256}"
        return sn

    def get_maximum_solar_power_today(self):
        """Max solar power today"""
        return self.retriable_read_register(0x010F, 0, 3, False)

    @property
    def maximum_solar_power_today(self):
        """Maximum solar power"""
        return self.get_maximum_solar_power_today()
    
    def get_minimum_solar_power_today(self):
        """Min solar power today"""
        # FIXME, register 0x0110 is Max. discharging power
        # of the current day (ROVER_MODBUS.pdf)
        return self.retriable_read_register(0x0110, 0, 3, False)

    @property
    def minimum_solar_power_today(self):
        """Minimum solar power"""
        return self.get_minimum_solar_power_today()
    
    def get_maximum_battery_voltage_today(self):
        """Maximum solar power today [V]"""
        return self.retriable_read_register(0x010C, 1, 3, False)

    @property
    def maximum_battery_voltage_today(self):
        """Maximum solar voltage today [V]"""
        return self.get_maximum_battery_voltage_today()
    
    def get_minimum_battery_voltage_today(self):
        """Minimum solar power today"""
        return self.retriable_read_register(0x010B, 1, 3, False)

    @property
    def minimum_battery_voltage_today(self):
        """Minimum solar voltage today"""
        return self.get_minimum_battery_voltage_today()
    
    @property
    def max_charging_current(self):
        """Maximum charging current today [A]"""
        return self.retriable_read_register(0x010D, 2, 3, False)

    @property
    def max_charging_power(self):
        """Maximum charging power today"""
        return self.retriable_read_register(0x010F, 0, 3, False)

    @property
    def charging(self):
        """Charging [Ah] today"""
        return self.retriable_read_register(0x0111, 0, 3, False)

    @property
    def power_generation(self):
        """Power generated today [kWh]"""
        return self.retriable_read_register(0x0113, 4, 3, False)
    
    @property
    def max_discharging_current(self):
        """Max discharging current today [A]"""
        return self.retriable_read_register(0x010E, 2, 3, False)

    @property
    def max_discharging_power(self):
        """Max discharging power today"""
        return self.retriable_read_register(0x0110, 0, 3, False)

    @property
    def discharging(self):
        """Discharging today [Ah]"""
        return self.retriable_read_register(0x0112, 0, 3, False)

    @property
    def power_consumption(self):
        """Power consumed today [kWh]"""
        return self.retriable_read_register(0x0114, 4, 3, False)
        

    
