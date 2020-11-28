#******************************************************************************
#
# ENGR 133 - FA 20 - LC4-02
# Personal Project - Ethan Kessel (ekessel@purdue.edu)
#
# ENGR133_Project_circuitSim_funcs_ekessel.py
#
# This file contains some of the functions for the main script.
# Models an astable multivibrator oscilator circuit built using an op-amp using
# the integrate module of scipy.
#
#==============================================================================
#
# MIT License
#
# Copyright (c) 2020 Ethan Kessel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#******************************************************************************

import sys
import os
import numpy as np
import json
from types import SimpleNamespace # Container where values can be accessed like members

CONST_NAMES = {'C':'Farads',
               'R1':'Ohms',
               'R2':'Ohms',
               'R3':'Ohms',
               'GAIN':'dB',
               'VCC':'Volts',
               'VDD':'Volts',
               'VREF':'Volts',
               'T_0':'Seconds',
               'T_F':'Seconds',
               'T_S':'Seconds'}

# Validate the contents of a JSON file
def validateJSONconstants(path):
    with open(path) as fileobj:
        json_file = json.load(fileobj)
        if not all(key in json_file for key in CONST_NAMES):
            raise ValueError("JSON file missing neccesary parameters")

# Convert decibels to unitless voltage amplification
def dBtoAmp(decibels): return (10 ** (decibels / 20))

# Uses a lambda to create a function that behaves like an op-amp
def makeOpAmpFunc(gain, vcc, vdd = 0):
    if vcc <= vdd:
        raise ValueError("Vcc must have a higher potential than Vdd")
    return lambda ninv, inv : (np.clip((gain * (ninv - inv) + (vcc + vdd) / 2), vdd, vcc))

# Input values and calculate values
def userInputCalculate(defaults_fpath):
    with open(defaults_fpath) as fileobj: # Load defaults
        c = json.load(fileobj, object_hook = lambda d : SimpleNamespace(**d))
        
    modes = ["Input circuit values.", "Calculate RC constant for frequency/period."]
    print("\nPlease select a mode or 0 to exit:")
    for idx, option in enumerate(modes):
        print(f" {idx + 1}) {option}")
        
    while True:
        instr = input("Enter a mode -> ")
        try:
            inval = int(instr)
            if not (0 <= inval <= len(modes)):
                raise ValueError(f"Invalid entry: Please enter a number 0-{len(modes)}")
            break
        except ValueError as e:
            print(f"Error: {e}")
            
    if inval == 0: # Exit
        print("Exiting...")
        sys.exit()
    elif inval == 1: # Enter values manually
        print("For each of the values below, enter a positive value or leave blank for the default:")
        for val_name in CONST_NAMES:
            unit_name_len = len(CONST_NAMES[val_name]) # For making it look good
            instr = input(f" {val_name:<4} (Default = {c.__getattribute__(val_name):7} [{CONST_NAMES[val_name]}]) {(8 - unit_name_len) * '-'}> ")
            try:
                new_val = float(instr)
                c.__setattr__(val_name, new_val)
            except ValueError:
                pass
    else:
        print("In order to calcuate for a specific frequency or period, the default values will be used for most constants.")
        valid_cnames = ['GAIN', 'T_0', 'T_F', 'T_S']
        print("For each of the values below, enter a positive value or leave blank for the default:")
        for val_name in valid_cnames:
            unit_name_len = len(CONST_NAMES[val_name]) # For making it look good
            instr = input(f" {val_name:<4} (Default = {c.__getattribute__(val_name):7} [{CONST_NAMES[val_name]}]) {(8 - unit_name_len) * '-'}> ")
            try:
                new_val = float(instr)
                c.__setattr__(val_name, new_val)
            except ValueError:
                pass
         
        while True:
            instr = input("Please select [f]requency or [p]eriod -> ").lower()
            if instr == 'f':
                prompt = "frequency [Hz]"
                convert = lambda inp : 1 / inp
                break
            elif instr == 'p':
                prompt = "period [s]"
                convert = lambda inp: inp
                break
            print("Please enter 'f' or 'p' only.")
            
        while True:
            instr = input(f"Enter the desired {prompt} -> ")
            try:
                inval = float(instr)
                if inval <= 0:
                    raise ValueError("Value must be positive")
                period = convert(inval)
                break
            except ValueError as e:
                print(f"Error: {e}")
                
        RC = period / (2 * np.log(3))
        print(f"The needed RC time constant is {RC:.3f} [Ohm-Farads].")
        
        while True:
            instr = input("Please select whether to fix [r]esistance or [c]apacitance -> ").lower()
            if instr == 'r':
                prompt = "resistance [Ohms]"
                calculate = lambda R : (R, RC / R)
                break
            elif instr == 'c':
                prompt = "capacitance [Farads]"
                calculate = lambda C : (RC / C, C)
                break
            print("Please enter 'r' or 'c' only.")
            
        while True:
            instr = input(f"Enter the desired {prompt} -> ")
            try:
                inval = float(instr)
                if inval <= 0:
                    raise ValueError("Value must be positive")
                R, C = calculate(inval)
                break
            except ValueError as e:
                print(f"Error: {e}")
                
        c.C = C
        c.R1 = R                
    
    return c

# Compute information about the oscillation of the circuit based on the constants
def computeFrequencyParams(c):
    t_high = c.R1 * c.C * (np.log(1 - (((c.VDD - c.VREF) * c.R2) /
                                  ((c.R2 + c.R3) * (c.VCC - c.VREF)))) -
                           np.log(1 - (c.R2 / (c.R2 + c.R3))))
    t_low  = c.R1 * c.C * (np.log(1 - (((c.VCC - c.VREF) * c.R2) /
                                  ((c.R2 + c.R3) * (c.VDD - c.VREF)))) -
                           np.log(1 - (c.R2 / (c.R2 + c.R3))))
    period = t_high + t_low
    frequency = 1 / period
    duty_cycle = t_high / period
    
    return frequency, period, duty_cycle, t_high, t_low
