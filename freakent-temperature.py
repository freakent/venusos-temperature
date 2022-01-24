#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import dbus
import dbus.service
import inspect
import pprint
import os
import sys

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../'))
from vedbus import VeDbusService

softwareVersion = '1.0'

def validate_new_value(path, newvalue):
	# Max RPM setpoint = 1000
	return newvalue <= 1000

def get_text_for_rpm(path, value):
	return('%d rotations per minute' % value)

def main(argv):
		global dbusObjects

		print(__file__ + " starting up")

		# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
		DBusGMainLoop(set_as_default=True)

		# Put ourselves on to the dbus
		dbusservice = VeDbusService('com.victronenergy.temperature.tty02')

		# dbusservice.__del__()

		dbusservice.add_mandatory_paths(
			processname=__file__,
			processversion=softwareVersion,
			connection='tty02',
			deviceinstance=300,
			productid=41312,
			productname='Freakent Temperature Sensor',
			firmwareversion='v1.0',
			hardwareversion='v1.0',
			connected=1)

		# Most simple and short way to add an object with an initial value of 5.
		dbusservice.add_path('/CustomName', 'FreakEnt Temp Sensor')
		dbusservice.add_path('/TemperatureType', 2)
		dbusservice.add_path('/Temperature', value=5, description="Cabin temperature", writeable=True)
		dbusservice.add_path('/Humidity', value=59.56, description="Cabin humidity", writeable=True)
		#dbusservice.add_path('/Pressure', value=None, description="Cabin pressure", writeable=True)

		# Most advanced wayt to add a path
		#dbusservice.add_path('/RPM', value=100, description='RPM setpoint', writeable=True,
			#onchangecallback=validate_new_value, gettextcallback=get_text_for_rpm)

		# You can access the paths as if the dbusservice is a dictionary
		print('/Temperature value is %s' % dbusservice['/Temperature'])

		# Same for changing it
		#dbusservice['/Temperature'] = 10

		print('/Temperature value is now %s' % dbusservice['/Temperature'])

		# To invalidate a value (see com.victronenergy.BusItem specs for definition of invalid), set to None
		#dbusservice['/Position'] = None

		# dbusservice.add_path('/String', 'this is a string')
		# dbusservice.add_path('/Int', 0)
		# dbusservice.add_path('/NegativeInt', -10)
		# dbusservice.add_path('/Float', 1.5)
   
		mainloop = GLib.MainLoop()
		mainloop.run()

main("")
