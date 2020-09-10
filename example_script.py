# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 2020

@author:    K. R. Williamson
            <kevin.williamson@nist.gov>
            
Continuous stabilization of large metal box by a 585 TECPak from Arroyo 
Instruments, Inc.

Sets up TEC controller

Logs data to file in CSV format
Plots the last 5 hours of live data continously
Keyboard Interrupt (^C) ends plotting, saves data, and turns off TEC source
"""

# serial_interface.py must be in the same directory as example_script.py
import os
print(os.getcwd())

import csv
from serial_interface import arroyo
from time import sleep
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

# Create an object for the TEC controller which opens up serial com w/ instr.
# The command line interface will print all available arroyo devices in a 
#   number list. Type the number of the instrument you wish to use and hit
#   "enter".
TECpak586 = arroyo()
set_point = 23.0
TECpak586.set_mode("T")
TECpak586.set_heatcool("BOTH")
TECpak586.set_current_limit(4.7)
TECpak586.set_voltage_limit(23.0)

# Set some restrictions on outputs and setpoints
TECpak586.set_fan("OFF",1)
TECpak586.set_TLO_limit(-1.0)
TECpak586.set_THI_limit(35.0)

# Sets tolerance spec for controller
TECpak586.set_tolerance(0.01, 5)

# Sets control type to PID and sets values, tune to your application
TECpak586.set_gain("PID")
TECpak586.set_PID(32, 0.031, 0)

# Turns on output and sets temperature control point 
TECpak586.set_output(1)
TECpak586.set_temp(set_point)

# Creating active graph to continously plot the most recent 5 hours of data
run_start = datetime.now()
run_length = timedelta(0)
t = []
target = []
temperature = []
V_out = []
I_out = []
P_out = []
t.append(datetime.now())
target.append(set_point)
temperature.append(TECpak586.read_temp())
V_out.append(TECpak586.read_voltage())
I_out.append(TECpak586.read_current())
P_out.append(I_out[-1] * V_out[-1])
sleep(0.9)
t.append(datetime.now())
target.append(set_point)
temperature.append(TECpak586.read_temp())
V_out.append(TECpak586.read_voltage())
I_out.append(TECpak586.read_current())
P_out.append(I_out[-1] * V_out[-1])
sleep(0.9)

fig1 = plt.figure(figsize=(4,3),dpi=150)
ax1 = fig1.add_subplot(2,2,1)
ax1.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30))
ax1.set_ylim(22.9, 23.1)
temp_line, = ax1.plot(t, temperature, 'r.')
target_line, = ax1.plot(t, target, 'b--')
ax1.set_title("WETCAT Thermistor")
ax1.set_xlabel("Time (Date then hour)")
ax1.set_ylabel("Temperature [\u00b0C]")

ax2 = fig1.add_subplot(2,2,4)
ax2.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30))
ax2.set_ylim(-5.0, 5.0)
I_line, = ax2.plot(t, I_out, 'b.')
#ax2.set_title("Controller Current")
ax2.set_xlabel("Time (Date then hour)")
ax2.set_ylabel("Output Current [Amps]")

ax3 = fig1.add_subplot(2,2,3)
ax3.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30))
ax3.set_ylim(-21.0, 21.0)
V_line, = ax3.plot(t, V_out, 'g.')
#ax3.set_title("Controller Voltage")
ax3.set_xlabel("Time (Date then hour)")
ax3.set_ylabel("Output Voltage [Volts]")

ax4 = fig1.add_subplot(2,2,2)
ax4.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30))
ax4.set_ylim(0, 50)
P_line, = ax4.plot(t, P_out, 'g.')
#ax4.set_title("Bulk Power Supply")
ax4.set_xlabel("Time (Date then hour)")
ax4.set_ylabel("Output Electrical Power [Watts]")

# Logs and plots data user enters keyboard interrupt (^C) into terminal
with open(str(t[0])[0:10] + '_data_log', mode='w') as data_log:
    data_writer = csv.writer(data_log, delimiter=',')
    data_writer.writerow(["Timestamp","Target","Temperature","Current","Voltage","Power"])
    try:    # a keyboard interup is used to stop data collection and initiate the turning off of the controller.
        while True:
            t.append(datetime.now())
            target.append(set_point)
            temperature.append(TECpak586.read_temp())
            V_out.append(TECpak586.read_voltage())
            I_out.append(TECpak586.read_current())
            P_out.append(I_out[-1] * V_out[-1])
            temp_line.set_xdata(t)
            temp_line.set_ydata(temperature)
            target_line.set_xdata(t)
            target_line.set_ydata(target)
            I_line.set_xdata(t)
            I_line.set_ydata(I_out)
            V_line.set_xdata(t)
            V_line.set_ydata(V_out)
            P_line.set_xdata(t)
            P_line.set_ydata(P_out)
            ax1.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
            ax2.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
            ax3.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
            ax4.set_xlim( t[0] - timedelta(seconds=30), t[-1] + timedelta(seconds=30) )
            plt.pause(0.9)
            run_length = datetime.now() - run_start
            # 5 hours length for plotting and storage within python
            # Data is trimmed continuously after 18000 seconds (5 hours)
            if len(t) > 18000:
                t = t[1:]
                target = target[1:]
                temperature = temperature[1:]
                V_out = V_out[1:]
                I_out = I_out[1:]
                P_out = P_out[1:]
            # Store more recently aquired data from each measurement
            data_writer.writerow([t[-1],target[-1],temperature[-1],
                                  I_out[-1],V_out[-1],P_out[-1]])
    except KeyboardInterrupt:
        pass

# Saves png of figure
plt.savefig(str(t[-1])[0:10] + 'figure.png')

# Closes communication with the instrument... Don't forget to do this!
TECpak586.set_output(0)
TECpak586.close()
