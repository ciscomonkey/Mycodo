# Mycodo: An environmental monitoring and regulation system

### Latest version: 4.0.0

Mycodo consists of a central server and a web-enabled user interface. Its function is to enable monitoring of sensors and conduct manipulation of relays to regulate environmental conditions. Regulation is accomplished with discrete PID controllers, enabling fine-control of the output.

Want to maintain your beer fermenter at a specific temperature?
Want to change your reptile enclosure temperature, humidity, and CO2 at times of the day?
Need to incubate chicken eggs or other premature animals with a live video feed?
Traveling and need your garden irrigated when the soil is dry?

Originally developed for cultivating gourmet mushrooms, its use has since broadened to include various other purposes, including cultivating plants, aging cheeses, incubating snake eggs and mice, regulating herptariums, and regulating a [laboratory honey bee apiary](https://www.youtube.com/watch?v=y2KLUmvZQhg) for scientific research, to name a few.

[![Mycodo](http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/05/Mycodo-3.6.0-tango-Graph-2016-05-21-11-15-26.png)](http://kylegabriel.com/projects/)


## Table of Contents

- [Features](#features)
- [TODO](#todo)
- [Supported Devices and Sensors](#supported-devices-and-sensors)
    - [Temperature](#temperature)
    - [Humidity](#humidity)
    - [CO<sub>2</sub>](#co2)
    - [Pressure](#pressure)
    - [Luminosity](#luminosity)
    - [Devices](#devices)
- [Notes](#notes)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Enable I2C](#enable-i2c)
    - [Influxdb](#influxdb)
    - [Databases](#databases)
    - [HTTP Server](#http-server)
    - [Final Steps](#final-steps)
- [Daemon Info](#daemon-info)
- [Web UI](#web-ui)
- [Upgrading](#upgrading)
- [Restoring Backups](#restoring-backups)
- [License](#license)
- [Screenshots](#screenshots)
- [Links](#links)


## Features

* Python daemon that controls sensors, relays, PIDs, LCDs, timers, and other aspects of the system.
* Web interface (Flask) for configuring, activating, and deactivating componenets of the system.
* Automated sensor reading and writing to influxdb (round-robin) database.
* Discrete PID control of devices connected to relays from sensor data to regulate environmental conditions.
* Dynamic PID setpoints to change at specific times or spans of the day.
* Dashboard with custom graphs for displaying any combination of sensor measurements and relays together.
* Log controllers that periodically save data from influxdb to text file in CSV format.
* 16x2 and 20x4 I<sup>2</sup>C LCD support (display latest sensor measurement time/date or value on each line).
* TCA9548A I<sup>2</sup>C multiplexer support for sensors and LCDs.
* Relay and Sensor conditionals that act in response to relay actions or sensor measurements, which can modulate relays, execute commands, and send email notifications.
* SQLite database migration (alembic) to upgrade an old mycodo database to work with the current Mycodo version.
* Update system from UI or command line (update SQL databases, update Mycodo from github).
* Pi Camera support (still and video stream, timelapse coming soon)


## TODO:

* Add graph export options (width, height, scale)
* Create custom log from influxdb query
* Notes, flag points of time on graph (text, file upload, graph saving, etc.).


## Supported Devices and Sensors

Certain sensors will require extra steps to be taken in order to set up the interface to communicate with them. The DS18B20 needs one-wire support enabled and the K30 will require configuring UART.

### Temperature

> [DS18B20](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing)

The DS18B20 is a simple 1-wire sensor. Once the one-wire interface has been configured with the above instructions, it may be used with Mycodo.

> [TMP 006/007](https://www.sparkfun.com/products/11859)

The TMP006 (and 007) can measure the temperature of an object without making contact with it, by using a thermopile to detect and absorb the infrared energy an object is emitting. This sensor also measures the temperature of the die (physical sensor).

### Humidity

> [DHT11, DHT22, AM2302](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring)

> [AM2315](https://github.com/lexruee/tentacle_pi)

> [SHT10, SHT11, SHT15, SHT71, SHT75](https://github.com/mk-fg/sht-sensor)

NOTE: The Raspberry Pi uses 3.3-volts for powering the SHT sensor, however the default driver (sht-sensor) does not handle measurement calculations from 3.3-volts, only 3.5-volts. This can be easy corrected by setting the correct coefficient in driver (a future revision will fix this).

### Carbon Dioxide (CO<sub>2</sub>)

> [K30](http://www.co2meters.com/Documentation/AppNotes/AN137-Raspberry-Pi.zip)

This documentation provides specific installation procedures for the K30 with the Raspberry Pi as well as example code. Once the K30 has been configured with this documentation, it can be tested whether the sensor is able to be read, by executing mycodo/tests/Test-Sensor-CO2-K30.py

UART is handled differently with the Raspberry Pi 3, because of bluetooth. Therefore, follow the instructions in the above link for Raspberry Pis 1 and 2, and the following instructions for the Raspberry pi 3:

Run raspi-config, go to Advanced Options->Serial and disable.

```sudo raspi-config```

edit /boot/config.txt and find the line "enable_uart=0" and change it to "enable_uart=1", then reboot.

### Pressure

> [BMP085/BMP180](https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi)

### Luminosity

> [TSL2561](https://www.sparkfun.com/products/12055)

The TSL2561 SparkFun Luminosity Sensor Breakout is a sophisticated light sensor which has a flat response across most of the visible spectrum. Unlike simpler sensors, the TSL2561 measures both infrared and visible light to better approximate the response of the human eye. And because the TSL2561 is an integrating sensor (it soaks up light for a predetermined amount of time), it is capable of measuring both small and large amounts of light by changing the integration time.

The TSL2561 is capable of direct I2C communication and is able to conduct specific light ranges from 0.1 - 40k+ Lux easily. Additionally, the TSL12561 contains two integrating analog-to-digital converters (ADC) that integrate currents from two photodiodes, simultaneously.

### Edge Detection

The detection of a changing digital signal (for instance, HIGH to LOW) requires the use of edge detection. The rising edge (LOW to HIGH), the falling edge (HIGH to LOW), or both can be used to trigger events. The GPIO chosen to detect the signal should be equiped with an appropriate resistor that either pulls the GPIO up (connected to power) or down (connected to ground). The option to enable the internal pull-up or pull-down resistors is not available for safety reasons. Use your own resistor to pull the GPIO high or low.

Examples of devices that can be used with edge detection: simple switches and buttons, PIR motion sensors, reed switches, hall effect sensors, float switches, and more.

### Devices

> [TCA9548A I2C Multiplexer](https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/overview)

The TCA9548A I<sup>2</sup>C allows multiple sensors that have the same I<sup>2</sup>C address to be used with mycodo (such as the AM2315). The multiplexer has a selectable address, from 0x70 through 0x77, allowing up to 8 multiplexers to be used at once. With 8 channels per multiplexer, this allows up to 64 devices with the same address to be used.

> [MCP243x Analog to Digital Converter](http://www.dfrobot.com/wiki/index.php/MCP3424_18-Bit_ADC-4_Channel_with_Programmable_Gain_Amplifier_(SKU:DFR0316))

An analog to digital converter (ADC) allows the use of any analog sensor that outputs a variable voltage. The detectable voltage range of this ADC is &plusmn;2.048 volts. A [voltage divider](https://learn.sparkfun.com/tutorials/voltage-dividers) may be necessary for your sensor's output to fall within this range.

The MCP3424 is one of the low noise and high accuracy 18-Bit delta-sigma analog-to-digital (ΔΣ A/D) converter family members of the MCP342X series. Its characteristic is: Self calibration of internal offset and gain per each conversion. The user can select the resolution (12, 14, 16, or 18-bit) before the analog-to-digital conversion takes place. This allows the device to convert a very weak input signal with high resolution.


## Notes

A minimal set of anonymous usage statistics are collected to help improve development. No identifying information is saved from the information that is collected and it is only used to improve Mycodo. No other sources will have access to this information. The data collected is mainly how much specific features are used, how often errors occur, and other similar statistics. The data that's collected can be viewed from the 'View collected statistics' link in the Settings/General panel of the UI or at Mycodo/databases/statistics.csv. You may opt out from transmitting this information from the General settings in the Admin panel.

mycodo/scripts/mycodo_wrapper is a binary executable used to start the mycodo daemon, create and restore backups, and update the system, from the web interface. It has the setuid bit to permit it to be executed as root ('sudo update_mycodo.sh initialize' sets the correct permissions and setuid). Since shell scripts cannot be setuid (ony binary files), the mycodo_wrapper binay permits these operations to be executed as root by a non-root user (in this case, anyone belogning to the group 'mycodo'). You can audit the source code of mycodo/scripts/mycodo_wrapper.c and if you want to ensure the binary is indeed compiled from that source, you may compile it yourself with the following command. Otherwise, the compiled binary is already included and no further action is needed. I mention this to explain the need for setuid, for transparency, for security, and to maintain all code of this project as open source.

```sudo gcc ~/Mycodo/mycodo/scripts/mycodo_wrapper.c -o ~/Mycodo/mycodo/scripts/mycodo_wrapper```


## Installation

### Prerequisites

These install procedures assume you are using a Raspberry Pi with a fresh install of [Raspbian Jessie](https://www.raspberrypi.org/downloads/raspbian/).

```sudo raspi-config```

 + Change the default user (pi) password
 + Set the locale to en_US.UTF-8
 + Set the timezone (required for setting the proper time)
 + Enable I<sup>2</sup>C (required)
 + Enable Pi Camera support (optional)
 + Advanced A2: change the hostname (optional)
 + Expand the file system (required)
 + Reboot

**Warning! Do not skip the reboot and file system expansion! This needs to be done before continuing to install anything or there won't be any free space.**

```
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y
sudo apt-get install -y git libffi-dev libi2c-dev python-dev python-setuptools python-smbus sqlite3 vim
sudo easy_install pip
```

```
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make -j4
sudo make install
```

If you plan to use the DHT11, DHT22, or AM2302, you must add pigpiod to cron to start at boot. Edit the cron file with:

```sudo crontab -e```

Then add this line to the bottom of the file, then save and reboot:

```@reboot /usr/local/bin/pigpiod &```

```
cd
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```

```
cd
git clone https://github.com/kizniche/Mycodo
cd Mycodo
sudo pip install -r requirements.txt --upgrade
sudo useradd -M mycodo
sudo adduser mycodo gpio
```


### Enable I2C

Enable I<sup>2</sup>C support through raspi-config (and other options if not already done)

Edit /etc/modules and add 'i2c-bcm2708' to the last line of the file

```sudo vim /etc/modules```

Edit /boot/config.txt

```sudo vim /boot/config.txt```

and add the following two lines to the end of the file

```
dtparam=i2c1=on
dtparam=i2c_arm=on
```

Reboot

```sudo shutdown now -r```


### Influxdb

```
wget https://dl.influxdata.com/influxdb/releases/influxdb_0.13.0_armhf.deb
sudo dpkg -i influxdb_0.13.0_armhf.deb
sudo service influxdb start
```

Create the InfluxDB database, user, and password from the influxdb console.

```
influx
CREATE DATABASE "mycodo_db"
CREATE USER "mycodo" WITH PASSWORD 'mmdu77sj3nIoiajjs'
exit
```


### Databases

```~/Mycodo/init_databases.py -i all```

Add an Administrator to the User Database

```~/Mycodo/init_databases.py -A```


### HTTP Server

If you want write access to the mycodo files, add your user to the mycodo group, changing 'username' to your user.

```sudo usermod -a -G mycodo username```

The following steps will allow the Mycodo Flask application to run on Apache2 using mod_wsgi.

```
sudo apt-get install -y apache2 libapache2-mod-wsgi
sudo a2enmod wsgi ssl
sudo ln -s ~/Mycodo /var/www/mycodo
sudo cp ~/Mycodo/mycodo_flask_apache.conf /etc/apache2/sites-available/
sudo ln -sf /etc/apache2/sites-available/mycodo_flask_apache.conf /etc/apache2/sites-enabled/000-default.conf
mkdir ~/Mycodo/mycodo/frontend/ssl_certs
```

[letsencrypt.org](https://letsencrypt.org) provides free verified SSL certificates. However, if you don't want to bother, or don't have a domain, use the following commands to generate them locally (Note that this certificate will not be verified and you will have warning messages about the security of your site, unless you add the certificate to your browser's trusted list).

```cd ~/Mycodo/mycodo/frontend/ssl_certs/```

```openssl req -new -x509 -sha512 -days 365 -nodes -out cert.pem -keyout privkey.pem```

```openssl genrsa -out certificate.key 1024```

```openssl req -new -key certificate.key -out certificate.csr```

```openssl x509 -req -days 365 -in certificate.csr -CA cert.pem -CAkey privkey.pem -set_serial $RANDOM -out chain.pem```

```rm certificate.csr```


### Final Steps

Create the proper permissions for Mycodo (Very Important!)

```sudo ~/Mycodo/mycodo/scripts/update_mycodo.sh initialize```

Install and use the systemd script

```
sudo systemctl enable ~/Mycodo/mycodo/scripts/mycodo.service
sudo service mycodo start
```

Restart apache2

```sudo /etc/init.d/apache2 restart```

The login page can be found at https://localhost/ (note the 's' in https)



### Daemon info

The status of the daemon's service can be checked

```sudo service mycodo service```

The daemon can also be started manually if the systemd method above isn't used or an error needs to be debugged

```sudo ~/Mycodo/mycodo/mycodo_daemon.py```

Also, use '-d' to log all debug messages to /var/log/mycodo/mycodo.log

```sudo ~/Mycodo/mycodo/mycodo_daemon.py -d```



## Web UI

Add and start controllers

Relays and controllers (sensor, PID, LCD, log, and timer) can now be added, modified, and deleted from the web UI.

Notes:

1) Relays must be added before the relay dropdowns of the sensor and PID controllers will be populated.

2) Sensors must be added before the sensor dropdown of the PID controllers will be populated.

3) Controllers must be deactivated before modification of their settings are possible.

4) You cannot activate a controller that uses a sensor if the associated sensor controller is not active.

5) You cannot deactivate a sensor controller if there is another controller active (e.g. PID, Log, LCD, etc.) that using it and is also active. You will be required to first deactivate them (a message will prompt you to automatically deactivate any dependent controllers).


### Upgrading

If you already have Mycodo installed (>=3.6.0), you can perform an upgrade to the latest version on github by either using the Admin/Update menu in the web UI or by issuing the following command at the terminal. Note: You must be a member of the group 'mycodo', else you will have to execute the following command as root. A log of the update process can be found at /var/log/mycodoupdate.log

```~/Mycodo/mycodo/scripts/mycodo_wrapper upgrade```

Upgrading the mycodo database is performed automatically during the upgrade process (Admin/Update), however it can also be performed manually with the following commands (Note: This does not create the database, only upgrade it. You must already have a database created in order to upgrade):

```cd ~/Mycodo/databases```

```alembic upgrade head```

Refer to the [alembic documentation](http://alembic.readthedocs.org/en/latest/tutorial.html) for other functions.



### Restoring Backups

A backup is made when the system is upgraded. If you need to restore a backup, do the following, changing the appropriate directory names:

```
sudo mv ~/Mycodo ~/Mycodo_old
sudo cp -a /var/Mycodo-backups/Mycodo-TIME-COMMIT ~/Mycodo
sudo service mycodo restart
sudo /etc/init.d/apache2 restart
```


### License

Mycodo is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Mycodo is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/licenses/gpl-3.0.en.html) for more details.

A full copy of the GNU General Public License can be found at <a href="http://www.gnu.org/licenses/gpl-3.0.en.html" target="_blank">http://www.gnu.org/licenses/gpl-3.0.en.html</a>

This software includes third party open source software components: Discrete PID Controller. Each of these software components have their own license. Please see ./3.5/cgi-bin/mycodoPID.py for license information.


### Screenshots

Console output of the daemon running in debug mode (verbose output).

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/03/Mycodo-Console.png">

---

Status page displays all active sensors with a collapsable menu of activated PIDs and associated relays.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Status-2016-04-10-10-53-58.png">

---

Custom graphs can be created with specific measurements and relays displayed (also duration, height, width).

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Graph-2016-04-14-18-29-24.png">

---

The sensor controller page lists activated and deactivated sensor controllers and their conditionals.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Sensors-2016-04-10-10-52-36.png">

---

The relay page lists available relays and their conditionals.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Relays-2016-04-10-10-52-57.png">

---

The PID page lists activated and deactivated PID controllers.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-PID-2016-04-10-10-53-11.png">

---

Timers can be set to occurr at a specific time of day or on a timed schedule.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Timers-2016-04-14-18-33-24.png">

---

Log controllers enable polling of the influxdb at specific periods to create a log file.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Logs-2016-04-15-10-45-09.png">

---

The LCD page lists activated and deactivated LCD controllers.

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-LCD-2016-04-10-10-53-38.png">

---

Settings pages to modify miscelaneous settings SQL databases

<img src="http://kylegabriel.com/projects/wp-content/uploads/sites/3/2016/04/Mycodo-Alerts-Settings-2016-04-10-11-50-29-e1460303466599.png">

## Links

Thanks for using and supporting Mycodo, however it may not be the latest version or it may have been altered if not obtained through an official distribution site. You should be able to find the latest version on github or my web site.

https://github.com/kizniche/Mycodo

http://KyleGabriel.com
