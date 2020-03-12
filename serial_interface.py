# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:05:04 2020

@author:    Kevin Reed Williamson
            kevin.williamson@nist.gov
            National Inst. of Standards and Tech.
            Bldg 222 Room A145

Code to initiate communication and control TEC Controller 3510 from Arroyo 
Instruments, Inc.

"""

import serial
import serial.tools.list_ports as port_list
import numpy as np
from time import sleep 



class arroyo5310(object):
    """ Class to control Arroyo Instrument's TEC Controller 6310 """


    def __init__(self):
        """ Sets up connection to Arroyo device
        Searches through available COM connections and chooses 5310
        """
        # Listing all available COM ports on windows computer
        ports = list(port_list.comports())
        for p in ports:
            print (p)
            # Choosing COM port from list of available connections 
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
                        print("\n" + self.port + " has been opened.\n")
                        self.ser.write(b'*IDN? \r\n')
                        sleep(0.1)
                        print(bytes.decode(self.ser.read(256)))
                    else:
                        print("\nDid not connect to " + self.port + "\n")
                    return
                except:
                    print("Failed to connect to " + p[0])


    def write_command(self,command):
        """Takes in string type AT command and returns string type responce"""
        responce = None
        self.ser.write(str.encode(command) + b'\r\n')
        sleep(0.1)
        responce = bytes.decode(self.ser.read(256))
        return(responce)


    def beep(self):
        """ Makes a single beep from the controller 
            Seems to not work for my unit """
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
        """ Queries temperature read by 5310 and returns float in Celsius """
        temp = float(self.write_command("TEC:T? "))
        return(temp)


    def read_set_temp(self):
        """ Queries temperature set point from 5310 and returns a float value 
            in Celsius """
        set_point = float(self.write_command("TEC:SET:T? "))
        return(set_point)


    def set_temp(self, set_point):
        """ Writes new temperature set point for controller """
        self.write_command("TEC:T " + str(set_point) + " ")
        sleep(0.1)
        if set_point == self.read_set_temp():
            print("Updated set point to: " + str(set_point) + "\xb0C")
            return True
        else:
            print("Failed to update set point!")
            return False


    def read_tolerance(self):
        """ Query the TEC tolerance criteria 
            returns float type of tolerance in Celsius and time window
            in seconds 
            tolerance = 0.01 to 10 C
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
            print("Updated controller gain to: " + gain)
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
    

    def read_V_limit(self):
        """ Queries the voltage limit of the controller and returns
            it as float type value 
            Only available for v3.X firmware """
        limit = float(self.write_command("TEC:LIM:V? "))
        return(limit)


    def set_V_limit(self, vlim):
        """ Sets the maximum voltage over the peltier modules
            Only available for v3.X firmware """
        self.write_command("TEC:LIM:V " + str(vlim) + " ")
        sleep(0.1)
        if vlim == self.read_V_limit():
            print("Updated Voltage limit to: " + str(vlim))
            return True
        else:
            print("Failed to set Voltage limit!")
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
        
        
        if float(speed) == float(speed_new):
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