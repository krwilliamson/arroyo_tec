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
