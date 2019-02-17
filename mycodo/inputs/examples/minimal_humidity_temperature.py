# coding=utf-8
import logging

from mycodo.inputs.base_input import AbstractInput
from mycodo.inputs.sensorutils import calculate_dewpoint


# Measurements
measurements_dict = {
    0: {
        'measurement': 'temperature',
        'unit': 'C'
    },
    1: {
        'measurement': 'humidity',
        'unit': 'percent'
    },
    2: {
        'measurement': 'dewpoint',
        'unit': 'C'
    }
}

# Input information
# See the inputs directory for examples of working modules.
# The following link provides the full list of options with descriptions:
# https://github.com/kizniche/Mycodo/blob/single_file_input_modules/mycodo/inputs/examples/example_all_options_temperature.py
INPUT_INFORMATION = {
    'input_name_unique': 'TEST_00',
    'input_manufacturer': 'AAA Company X',
    'input_name': 'Dummy Input 00',
    'measurements_name': 'Humidity/Temperature',
    'measurements_dict': measurements_dict,

    'options_enabled': [
        'period',
        'pre_output'
    ],
    'options_disabled': [
        'interface',
        'i2c_location'
    ],

    'dependencies_module': [
        ('pip-pypi', 'random', 'random')
    ],

    'interfaces': ['I2C'],
    'i2c_location': ['0x5c'],
    'i2c_address_editable': False
}


class InputModule(AbstractInput):
    """ Input support class """
    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__()
        self.logger = logging.getLogger("mycodo.inputs.dummy_input")

        if not testing:
            self.logger = logging.getLogger(
                "mycodo.inputs.{name_lower}_{id}".format(
                    name_lower=INPUT_INFORMATION['input_name_unique'].lower(),
                    id=input_dev.unique_id.split('-')[0]))
            self.interface = input_dev.interface

            # Load dependent modules
            import random
            self.random = random

            # Retrieve options
            # These options can be used here to initialize an I2C device or elsewhere in this class
            self.i2c_address = input_dev.i2c_location
            self.i2c_bus = input_dev.i2c_bus

    def get_measurement(self):
        """ Measures temperature and humidity """
        # Resetting these values ensures old measurements aren't mistaken for new measurements
        return_dict = measurements_dict.copy()

        # Actual input measurement code
        try:
            humidity = self.random.randint(0, 100)
            temperature = self.random.randint(0, 50)

            if self.is_enabled(0):
                return_dict[0]['value'] = temperature

            if self.is_enabled(1):
                return_dict[1]['value'] = humidity

            if (self.is_enabled(2) and
                    self.is_enabled(0) and
                    self.is_enabled(1)):
                return_dict[2]['value'] = calculate_dewpoint(
                    return_dict[0]['value'], return_dict[1]['value'])

            return return_dict
        except Exception as msg:
            self.logger.error("Exception: {}".format(msg))
