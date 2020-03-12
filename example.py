# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:42:46 2020

@author:    Kevin Reed Williamson
            <kevin.williamson@nist.gov>
            
Example settings script for TEC Controller 5310 from Arroyo Instruments, Inc.
"""

from serial_interface import arroyo5310
from time import sleep
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

# Create an object for the TEC controller which opens up serial com w/ instr.
TEC_controller = arroyo5310()
set_point = 23.0

# Set some restrictions on outputs and setpoints
TEC_controller.set_fan(12, 2)
TEC_controller.set_TLO_limit(15.0)
TEC_controller.set_THI_limit(30.0)

# Sets tolerance spec for controller, not very important
TEC_controller.set_tolerance(0.01, 5)

# Sets control type to PID and sets values
TEC_controller.set_gain("PID")
TEC_controller.set_PID(4.5, 0.0001, 0)

# Turns on output and sets temperature control point 
TEC_controller.set_output(1)
TEC_controller.set_temp(23.0)

# Creating active graph  
run_start = datetime.now()
run_length = timedelta(0)
run_time = timedelta(minutes=30)
temperature = []
target = []
t = []
t.append(datetime.now())
target.append(set_point)
temperature.append(TEC_controller.read_temp())
sleep(0.9)
t.append(datetime.now())
target.append(set_point)
temperature.append(TEC_controller.read_temp())
sleep(0.9)

fig1 = plt.figure(figsize=(4,3),dpi=150)
ax1 = fig1.add_subplot(1,1,1)
ax1.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
ax1.set_ylim(22.5, 24.5)
line1, = ax1.plot(t, temperature, 'r.')
line2, = ax1.plot(t, target, 'b--')
plt.title("Temperature of Thermistor")
plt.xlabel("Time (Date then hour)")
plt.ylabel("Temperature [\u00b0C]")

while run_length < run_time:
    t.append(datetime.now())
    target.append(set_point)
    temperature.append(TEC_controller.read_temp())
    line1.set_xdata(t)
    line1.set_ydata(temperature)
    line2.set_xdata(t)
    line2.set_ydata(target)
    ax1.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
    plt.draw()
    plt.pause(0.9)
    run_length = datetime.now() - run_start 

# Closes communication with the instrument... Don't forget to do this!
TEC_controller.set_output(0)
TEC_controller.close()


