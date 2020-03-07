# arroyo3510
## Description:
Importable class object for serial communication and control of TEC Controller 3510 from Arroyo Instruments, Inc.

## Dependencies:
psyserial
numpy
time

## Example:
    # With the serial_interface.py file in the same directory as  
    In [1]: pwd
    Out[1]: '\\Users\\krwil'
    
    In [2]: from serial_interface import arroyo5310
    
    In [3]: TEC_controller = arroyo5310()
    Out[3]: 
