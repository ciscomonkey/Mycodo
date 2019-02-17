# coding=utf-8
import logging

from flask_babel import lazy_gettext

from mycodo.inputs.base_input import AbstractInput


def constraints_pass_fan_seconds(mod_input, value):
    """
    Check if the user input is acceptable
    :param mod_input: SQL object with user-saved Input options
    :param value: value
    :return: tuple: (bool, list of strings)
    """
    errors = []
    all_passed = True
    # Ensure value is positive
    if value <= 0:
        all_passed = False
        errors.append("Must be a positive value")
    return all_passed, errors, mod_input


def constraints_pass_measure_range(mod_input, value):
    """
    Check if the user input is acceptable
    :param mod_input: SQL object with user-saved Input options
    :param value: float
    :return: tuple: (bool, list of strings)
    """
    errors = []
    all_passed = True
    # Ensure valid range is selected
    if value not in ['1000', '2000', '3000', '5000']:
        all_passed = False
        errors.append("Invalid rage")
    return all_passed, errors, mod_input


# Measurements
measurements_dict = {
    0: {
        'measurement': 'temperature',
        'unit': 'C'
    }
}

# Input information
INPUT_INFORMATION = {
    #
    # Required options
    #

    # Unique name (must be unique from all other inputs)
    'input_name_unique': 'SEN_TEMP_01',

    # Descriptive information
    'input_manufacturer': 'Company YY',
    'input_name': 'Temp Sen01',

    # Measurement information
    'measurements_name': 'Temperature',
    'measurements_dict': measurements_dict,

    # Web User Interface display options
    # Options that are enabled will be editable from the input options page.
    # Options that are disabled will appear on the input options page but not be editable.
    # There are several location options available for use:
    # 'location', 'gpio_location', 'i2c_location', 'bt_location', 'ftdi_location', and 'uart_location'
    'options_enabled': [
        'i2c_location',
        'ftdi_location',
        'uart_location',
        'custom_options',
        'period',
        'pre_output'
    ],
    'options_disabled': ['interface'],


    #
    # Non-required options
    #

    # Python module dependencies
    # This must be a module that is able to be installed with pip or apt (pypi, git, and apt examples below)
    # Leave the list empty if there are no dependencies
    'dependencies_module': [  # List of tuples
        ('pip-pypi', 'Adafruit_GPIO', 'Adafruit_GPIO'),
        ('pip-pypi', 'bluepy', 'bluepy==1.1.4'),
        ('pip-git', 'adafruit-bme280', 'git://github.com/adafruit/Adafruit_Python_BME280.git#egg=adafruit-bme280'),
        ('apt', 'whiptail', 'whiptail'),
        ('apt', 'zsh', 'zsh'),
        ('internal', 'file-exists /opt/mycodo/pigpio_installed', 'pigpio'),
        ('internal', 'pip-exists wiringpi', 'wiringpi'),
        ('internal', 'file-exists /usr/local/include/bcm2835.h', 'bcm2835')
    ],

    # Interface options: 'GPIO', 'I2C', 'UART', '1WIRE', 'BT', 'Mycodo', 'RPi'
    'interfaces': [  # List of strings
        'I2C',
        'UART'
    ],

    # I2C options
    # Enter more than one if multiple addresses exist.
    'i2c_location': [  # List of strings
        '0x01',
        '0x02'
    ],
    'i2c_address_editable': False,  # Boolean

    # UART options
    'uart_location': '/dev/ttyAMA0',  # String
    'baud_rate': 9600,  # Integer
    'pin_cs': 8,  # Integer
    'pin_miso': 9,  # Integer
    'pin_mosi': 10,  # Integer
    'pin_clock': 11,  # Integer

    # Bluetooth options
    'bt_location': '00:00:00:00:00:00',  # String
    'bt_adapter': 'hci0',  # String

    # Custom location options
    # Only one option, editable text box:
    'location': {
        'title': 'Host',
        'phrase': 'Host name or IP address',
        'options': [('127.0.0.1', '')]
    },
    # More than one option, selectable drop-down menu:
    # 'location': {
    #     'title': 'Location Name',
    #     'phrase': 'Location Description',
    #     'options': [('1', 'Option 1'),
    #                 ('2', 'Option 2'),
    #                 ('3', 'Option 3'),]
    # },

    # Host options
    'times_check': 1,  # Integer
    'deadline': 2,  # Integer
    'port': 80,  # Integer

    # Signal options
    'weighting': 0.0,  # Float
    'sample_time': 2.0,  # Float

    # Analog-to-digital converter options
    'analog_to_digital_converter': True,  # Boolean
    'adc_gain': [  # List of tuples
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (8, '8'),
        (16, '16')
    ],
    'scale_from_min': -4.096,  # Float
    'scale_from_max': 4.096,  # Float

    # Miscellaneous options
    'period': 15,  # Float
    'cmd_command': 'shuf -i 50-70 -n 1',  # String
    'ref_ohm': 0,  # Integer

    # The following options must either be a list of tuples or a list containing one string
    # 'several_options': [
    #     (1, 'option 1 name'),
    #     (2, 'option 2 name')
    # ],
    # 'one_option': ['12'],
    'resolution': [],  # List of tuples or string
    'resolution_2': [],  # List of tuples or string
    'sensitivity': [],  # List of tuples or string
    'thermocouple_type': [],  # List of tuples or string
    'sht_voltage': [  # List of tuples or string
        ('2.5', '2.5V'),
        ('3.0', '3.0V'),
        ('3.5', '3.5V'),
        ('4.0', '4.0V'),
        ('5.0', '5.0V')
    ],

    # Custom options
    # Values are stored as text, therefore if you require a float or integer,
    # cast it as such in the "Load custom options" section in __init__
    # Example: self.another_option = int(value)
    # Make sure your string represents the type you're attempting to cast
    'custom_options': [
        {
            'id': 'fan_modulate',
            'type': 'bool',
            'default_value': True,
            'name': lazy_gettext('Fan Off After Measure'),
            'phrase': lazy_gettext('Turn the fan on only during the measurement')
        },
        {
            'id': 'fan_seconds',
            'type': 'float',
            'default_value': 5.0,
            'constraints_pass': constraints_pass_fan_seconds,
            'name': lazy_gettext('Fan On Duration'),
            'phrase': lazy_gettext('How long to turn the fan on (seconds) before acquiring measurements')
        },
        {
            'id': 'measure_range',
            'type': 'select',
            'default_value': '5000',
            'options_select': [
                ('1000', '0 - 1000 ppmv'),
                ('2000', '0 - 2000 ppmv'),
                ('3000', '0 - 3000 ppmv'),
                ('5000', '0 - 5000 ppmv'),
            ],
            'constraints_pass': constraints_pass_measure_range,
            'name': lazy_gettext('Measurement Range'),
            'phrase': lazy_gettext('Set the measuring range of the sensor')
        }

    ]
}


class InputModule(AbstractInput):
    """ A dummy sensor support class """

    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__()
        self.logger = logging.getLogger("mycodo.inputs.{name_lower}".format(
            name_lower=INPUT_INFORMATION['input_name_unique'].lower()))

        if not testing:
            self.logger = logging.getLogger(
                "mycodo.inputs.{name_lower}_{id}".format(
                    name_lower=INPUT_INFORMATION['input_name_unique'].lower(),
                    id=input_dev.unique_id.split('-')[0]))
            self.interface = input_dev.interface

            #
            # Begin dependent modules loading
            #

            import random
            self.random = random

            #
            # Load optional settings
            #

            self.resolution = input_dev.resolution

            #
            # Load custom options
            #

            # Default values if user settings are not set
            self.fan_modulate = True
            self.fan_seconds = 5.0
            self.measure_range = '5000'

            # User values if user settings are set
            if input_dev.custom_options:
                for each_option in input_dev.custom_options.split(';'):
                    option = each_option.split(',')[0]
                    value = each_option.split(',')[1]
                    if option == 'fan_modulate':
                        self.fan_modulate = bool(value)
                    elif option == 'fan_seconds':
                        self.fan_seconds = float(value)
                    elif option == 'measure_range':
                        self.measure_range = value

            #
            # Initialize the sensor class
            #

            if self.interface == 'I2C':
                self.i2c_address = int(str(input_dev.i2c_location), 16)
                self.i2c_bus = input_dev.i2c_bus
                # self.sensor = dependent_module.MY_SENSOR_CLASS(
                #     i2c_address=self.i2c_address,
                #     i2c_bus=self.i2c_bus,
                #     resolution=self.resolution)

            elif self.interface == 'UART':
                # No UART driver available for this input
                pass

    def get_measurement(self):
        """ Gets the temperature and humidity """
        #
        # Copy measurements dictionary
        #

        return_dict = measurements_dict.copy()

        #
        # Begin sensor measurement code
        #

        return_dict[0]['value'] = self.random.randint(50, 70)

        #
        # End sensor measurement code
        #

        return return_dict
