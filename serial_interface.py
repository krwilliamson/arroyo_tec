# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 2020
Editted on Thu Sep 10 2020

@author:    K. R. Williamson
            kevin.williamson@nist.gov

# Arroyo TEC Controllers API #
## Description ##
Importable class object for serial communication and control of TEC 
Controllers from Arroyo Instruments, Inc.

## License ##
Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

## Purpose ##
This project allows users with Windows 10 to interact with their Arroyo 
Instruments TEC Controllers. This API allows users to read settings, features, 
and update them with python code.

The library is composed of:
* A python API to communicate with a RS232 or a USB port via a serial 
    interface.
* An example script initiating communication, choosing device settings, and 
    recording/plotting live data. 

## Testing ## 
This program has only been tested with Windows 10 and the units listed below. 
This code could be adapted for laser diode controllers supplied by Arroyo 
Instruments. Users with a different operating system, should adjust the 
__init__ function for their circumstances. For example, Linux systems use a 
different syntax for connected devices and require adjustments to the 
__init__ coding.

Tested on the following models:
    3510 TEC Source
    585-05-12 TECPak
    586-08-26 TECPak

## Dependencies ##
This program was developed with following python package versions.
* dpython-dateutil  2.8.1
* matplotlib        3.1.3
* numpy             1.19.1
* pyserial          3.4
* python            3.7.7
* vs2015_runtime    14.16.27012      
"""

import serial
import serial.tools.list_ports as port_list
import numpy as np
from time import sleep 



class arroyo(object):
    """ Class to control Arroyo Instrument's TEC Sources """


    def __init__(self):
        """ Sets up connection to Arroyo device
        Searches through available COM connections and chooses 5310
        """
        # Listing all available COM ports on windows computer
        ports = list(port_list.comports())
        options = []
        option = 1
        for p in ports:
            # Lists all available devices by Arroyo Instruments
            if "USB Serial Port" in p[1]:
                try:
                    self.port = p[0]
                    # Setting up and connecting to device
                    self.ser = serial.Serial(port =     self.port,
                                             baudrate = 38400,
                                             parity =   serial.PARITY_NONE,
                                             stopbits = serial.STOPBITS_ONE,
                                             bytesize = serial.EIGHTBITS,
                                             timeout =  0,
                                             write_timeout = 0)
                    if self.ser.is_open:
                        self.ser.write(b'*IDN? \r\n')
                        sleep(0.1)
                        # Shows the model of Arroyo Instrument
                        print("Option " + str(option) + ": " + 
                              bytes.decode(self.ser.read(256)))
                        options.append(p[0])
                        option += 1 
                        self.ser.close()
                        sleep(0.1)
                    else:
                        print("\nDid not connect to " + self.port + "\n")
                except:
                    print("Failed to connect to " + p[0])
        # Allows user to choose Arroyo instrument they would like to connect
        choice = None
        while choice == None:
            print("Which option would you like to connect to?\n" + 
                  "Press 1, 2, 3,... then hit ENTER: ")
            choice = int(input()) - 1
        self.port = options[choice]
        self.ser = serial.Serial(port =     self.port,
                                 baudrate = 38400,
                                 parity =   serial.PARITY_NONE,
                                 stopbits = serial.STOPBITS_ONE,
                                 bytesize = serial.EIGHTBITS,
                                 timeout =  0,
                                 write_timeout = 0)
        if self.ser.is_open:
            print("\n" + self.port + " has been opened.\n")
            self.ser.write(b'*IDN? \r\n')
            sleep(0.1)
        else:
            print("\nDid not connect to " + self.port + "\n")


    def write_command(self,command):
        """Takes in string type AT command and returns string type response"""
        response = None
        self.ser.write(str.encode(command) + b'\r\n')
        sleep(0.1)
        response = bytes.decode(self.ser.read(256))
        return(response)


    def beep(self):
        """ Makes a single beep from the controller """
        self.write_command("BEEP 1 ")
        return 


    def close(self):
        """ Closes serial connection with controller """
        self.ser.close()
        sleep(0.1)
        if not self.ser.is_open:
            print("\n" + self.port + " has been closed.\n")
        return


    def sensor_constants(self):
        """ Queries device for sensor constants and returns array of floats"""
        response = self.write_command("TEC:CONST? ")
        response = response.split(',')
        response = np.array(response, dtype=float)
        return(response)


    def set_sensor_constants(self, A, B, C):
        """ Writes values for sensor constants
            Takes in float values A, B, and C """
        print("Previous constants:    " + str(self.sensor_constants()))
        self.write_command("TEC:CONST " +
                           str(A) + ", " +
                           str(B) + ", " +
                           str(C))
        sleep(0.1)
        print("     New constants:    " + str(self.sensor_constants()))
        return


    def read_temp(self):
        """ Queries temperature read by device and returns float in 
            Celsius """
        temp = float(self.write_command("TEC:T? "))
        return(temp)


    def read_set_temp(self):
        """ Queries temperature set point from device and returns a float 
            value in Celsius """
        set_point = float(self.write_command("TEC:SET:T? "))
        return(set_point)


    def set_temp(self, set_point):
        """ Writes new temperature set point for controller """
        if self.read_mode() != "T":
            self.set_mode("T")
        self.write_command("TEC:T " + str(set_point) + " ")
        sleep(0.1)
        if set_point == self.read_set_temp():
            print("Updated set point to: " + str(set_point) + "\xb0C")
            return True
        else:
            print("Failed to update set point!")
            return False


    def read_tolerance(self):
        """ Query the source tolerance criteria 
            Returns float type of tolerance in Celsius and time window in 
            seconds 
                tolerance = 0.01 to 10°C
                time = 0.1 to 50 seconds """
        response = self.write_command("TEC:TOL? ").split(",")
        tolerance = float(response[0])
        time =  float(response[1])
        return(tolerance,time)


    def set_tolerance(self, tolerance, time):
        """ Takes float types
            tolerance = 0.01 to 10 C
            time = 0.1 to 50 seconds """
        print("Previous tolerances:    " + str(self.read_tolerance()))
        self.write_command("TEC:TOL " +
                           str(tolerance) + ", " +
                           str(time))
        sleep(0.1)
        print("     New tolerances:    " + str(self.read_tolerance()))
        return


    def run_time(self):
        """ Returns time that unit has been running """
        time = self.write_command("TIME? ")
        print("Unit has been running for " + time)
        return(time)


    def read_gain(self):
        """ Query the control loop gain or PID control 
            Returns str type value 1, 3, 5, 10, 30, 50, 100 ,300, PID """
        gain = self.write_command("TEC:GAIN? ")
        try:
            gain = (gain.split('\r'))[0]
            return(gain)
        except:
            print("Error reading gain.")
            return


    def set_gain(self, gain): 
        """ Sets control loop gain of controller or switches to PID mode
            Takes str type value 1, 3, 5, 10, 30, 50, 100 ,300, PID """
        self.write_command("TEC:GAIN " + str(gain) )
        sleep(0.1)
        if str(gain) == self.read_gain():
            print("Updated controller gain to: " + str(gain))
            return True
        else:
            print("Failed to update gain!")
            return False


    def read_PID(self):
        """ Reads the PID values of the controller and returns them as 
            float type values in order P I D"""
        response = self.write_command("TEC:PID? ")
        response = response.split(",")
        P, I, D = np.array(response, dtype=float)
        return(P, I, D)


    def set_PID(self, P, I, D):
        """ Writes controller PID values
            takes in P I D in order as float type values """
        print("Previous PID:    " + str(self.read_PID()))
        self.write_command("TEC:PID " +
                           str(P) + ", " +
                           str(I) + ", " +
                           str(D))
        sleep(0.1)
        print("     New PID:    " + str(self.read_PID()))
        return


    def read_output(self):
        """ Checks if the output is enabled or disabled
            returns True for enabled and
            returns False for disabled """
        output = int(self.write_command("TEC:OUT? "))
        return(output)


    def set_output(self, value):
        """ Sets the output of the TEC controller to on or off 
            receiving the value 1 sets the controller output to on
            receiving the value 0 sets the controller output to off"""
        self.write_command("TEC:OUT " + str(value))
        sleep(0.1)
        if value == self.read_output():
            print("Updated output to: " + str(value))
            return True
        else:
            print("Failed to set output!")
            return False


    def read_THI_limit(self):
        """ Queries the temperature limit of the controller and returns
            it as float type value """
        limit = float(self.write_command("TEC:LIM:THI? "))
        return(limit)


    def set_THI_limit(self, THIlim):
        """ Sets the maximum temperature at which the output remains on """
        self.write_command("TEC:LIM:THI " + str(THIlim) + " ")
        sleep(0.1)
        if THIlim == self.read_THI_limit():
            print("Updated Temperature High limit to: " + str(THIlim))
            return True
        else:
            print("Failed to set Temperature High limit!")
            return False


    def read_TLO_limit(self):
        """ Queries the temperature limit of the controller and returns
            it as float type value """
        limit = float(self.write_command("TEC:LIM:TLO? "))
        return(limit)


    def set_TLO_limit(self, TLOlim):
        """ Sets the minimum temperature at which the output remains on """
        self.write_command("TEC:LIM:TLO " + str(TLOlim) + " ")
        sleep(0.1)
        if TLOlim == self.read_TLO_limit():
            print("Updated Temperature Low limit to: " + str(TLOlim))
            return True
        else:
            print("Failed to set Tempearture Low limit!")
            return False


    def read_fan(self):
        """ Queries the controller for the status of the fan output
            speed returns str type OFF, SLOW, MEDIUM, FAST, or 4.0 to 12.0 in V
            mode returns int type 1, 2, or 3 (2 is always on)
            delay returns int type 1 to 240 in minutes """
        response = self.write_command("TEC:FAN? ")
        response = response.split(",")
        speed = response[0]
        mode = int(response[1])
        delay = int(response[2])
        return(speed, mode, delay)


    def set_fan(self, speed, mode, delay = None):
        """ Sets controller fan settings by taking 3 arguments 
            speed takes str value OFF, SLOW, MEDIUM, FAST, or 4.0 to 12.0 in V
            mode takes int type 1, 2, or 3 (2 is always on)
            delay takes int type 1 to 240 in minutes 
            recomend: arroyo.set_fan(12,2) """
        if not delay:
            self.write_command("TEC:FAN " + 
                               str(speed) + "," + 
                               str(mode))
        else:
            self.write_command("TEC:FAN " + 
                               str(speed) + "," + 
                               str(mode) + "," +
                               str(delay))
        sleep(0.1)
        speed_new, mode_new, delay_new = self.read_fan()
        
        if str(speed) == str(speed_new):
            print("Updated fan speed to: " + str(speed))
        else:
            print("Failed to update fan speed!")
        if int(mode) == mode_new:
            print("Updated fan mode to: " + str(mode))
        else:
            print("Failed to update fan mode!")
        if delay:
            if int(delay) == delay_new:
                print("Updated fan delay to: " + str(delay))
            else:
                print("Failed to update fan delay!")
        return()


    def read_mode(self):
        """ Queries the operation mode of the controller 
            Returns 1 of 3 string values:
                T   Temperature
                R   Resistance
                ITE Current """
        response = self.write_command("TEC:MODE? ").split("\r")[0]
        return(response)


    def set_mode(self, mode):
        """ Sets the operation mode of the controller 
            Takes 1 of 3 string values:
                T   Temperature
                R   Resistance
                ITE Current """
        print("Controller mode is set to: " + self.read_mode())
        self.write_command("TEC:MODE:" + mode + " ")
        if mode == self.read_mode():
            print("Controller mode updated to: " + mode)
        else:
            print("Failed to update controller mode!")
        return()


    def read_current(self):
        """ Queries the measured output value of the current
            Returns a float type value """
        response = float(self.write_command("TEC:ITE? "))
        return(response)


    def read_set_current(self):
        """ Queries the set point value of the current
            Returns a float type value """
        response = float(self.write_command("TEC:SET:ITE? "))
        return(response)


    def set_current(self, set_point):
        """ """
        if self.read_mode() != "ITE":
            self.set_mode("ITE")
        self.write_command("TEC:ITE " + str(set_point) + " ")
        if float(set_point) == self.read_set_current():
            print("Updated current set point to: " + str(set_point) + " Amps")
            return True
        else:
            print("Failed to update current set point!")
            return False


    def read_current_limit(self):
        """ Queries the maximum current output of the controller
            Returns a float type value """
        response = float(self.write_command("TEC:LIM:ITE? "))
        return(response)


    def set_current_limit(self, limit):
        """ Sets the maximum current output of the controller
            Takes a float type value up to 10 """
        print("Current limit is set to: " + 
              str(self.read_current_limit()) + " Amps")
        self.write_command("TEC:LIM:ITE " + str(limit) + " ")
        if float(limit) == self.read_current_limit():
            print("Updated current limit to: " + str(limit) + " Amps")
            return True
        else:
            print("Failed to set current limit!")
            return False


    def vbulk(self):
        """ Queries the unit's supply voltage """
        response = float(self.write_command("TEC:VBULK? "))
        return(response)


    def read_voltage(self):
        """ Queries the measured output value of the voltage
            Returns a float type value """
        response = float(self.write_command("TEC:V? "))
        return(response)


    def read_voltage_limit(self):
        """ Queries the voltage limit of the controller and returns
            it as float type value 
            Only available for v3.X firmware """
        limit = float(self.write_command("TEC:LIM:V? "))
        return(limit)


    def set_voltage_limit(self, vlim):
        """ Sets the maximum voltage over the peltier modules
            Only available for v3.X firmware """
        print("Voltage limit is set to: " + 
              str(self.read_voltage_limit()) + " Volts")
        self.write_command("TEC:LIM:V " + str(vlim) + " ")
        if float(vlim) == self.read_voltage_limit():
            print("Updated voltage limit to: " + str(vlim) + " Volts")
            return True
        else:
            print("Failed to set voltage limit!")
            return False


    def read_heatcool(self):
        """ Queries the unit heat/cool mode. Retunrs string type value:
                BOTH
                HEAT 
                COOL """
        mode = self.write_command("TEC:HEATCOOL? ").split("\r")[0]
        return(mode)


    def set_heatcool(self, mode):
        """ Sets the heat/cool mode of the unit. Command takes one of three 
            string type values:
                BOTH
                HEAT
                COOL """
        print("Heat/cool mode is set to: " + 
              str(self.read_heatcool()))    
        self.write_command("TEC:HEATCOOL " + str(mode))
        if str(mode) == self.read_heatcool():
            print("Updated heat/cool mode to: " + str(mode))
            return True
        else:
            print("Failed to set heat/cool mode!")
            return False


    def read_autotune(self):
        """ Queries autotune result since boot-up """
        response = int(self.write_command("TEC:AUTOTUNE? ").split("\r")[0])
        if response == 0:
            print("No AutoTune has been performed since last power-up")
            return(0)
        elif response == 1:
            print("AutoTune in process")
            return(1)
        elif response == 2:
            print("Last AutoTune failed")
            return(2)
        elif response == 3:
            print("Last AutoTune successful")
            return(3)
        else:
            print("COM error in read_autotune function")
            return(None)
    
    
    def autotune(self, test_point):
        """ The TEC:AUTOTUNE command is used to start the AutoTune process, 
        using the temperature parameter as the AutoTune point. The current and
        temperature limits should be properly setup prior to starting AutoTune.
        
        Takes one float type variable as the set point to be tested."""
        self.read_autotune()
        self.write_command("TEC:AUTOTUNE " + str(test_point) + " ")
        sleep(0.5)
        self.read_autotune()
        return()


    def read_autotunestate(self):
        """ Work in progress, feel free to write this one if you need it. :) """
        return()

        
        
        
