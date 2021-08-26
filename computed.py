# Waveform Computation Methods for TXo/TXo+
# (c) 2018 Brendon Cassidy; MIT Licensed

from __future__ import division
import math

def sawtooth(length=512):    
    
    raw_table = []  

    step = 65535. / length

    for index in range(length):
        
        value = (step * index) - 32768.
        raw_table.append(hex(int(value)))

    raw_table.append(raw_table[0])   
    return raw_table

def sine(length=512):    
    raw_table = []  
    for index, item in enumerate((math.sin(2*math.pi*i/length) for i in range(length))):
        if math.modf(item)[0] > 0.5:
            value = hex(int(math.ceil((item*0x7FFF))))
        else:
            value = hex(int(math.floor((item*0x7FFF))))

        raw_table.append(value)
    
    raw_table.append(raw_table[0])   
    return raw_table

def triangle(length=512):    
    raw_table = []  

    step = 65535. / (length / 2)
    reverse = length

    for index in range(length):
        
        if index < length / 2:
            value = (step * index) - 32768.
        else:
            value = (step * reverse) - 32768.

        raw_table.append(hex(int(value)))

        reverse = reverse - 1

    raw_table.append(raw_table[0])   
    return raw_table
