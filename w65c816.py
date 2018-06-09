#!/usr/bin/python3
from skidl import *
import os
import glob

# A            Assembly
# AR         Amplifier
# AT         Attenuator; Isolator
# B            Blower
# BR         Bridge Rectifier
# BT         Battery
# C            Capacitor
# CB         Circuit Breaker
# CN         Capacitor Network
# CP         Coupler
# CR         Diode or Silicon Rectifier
# D            Diode; Thyristor; Varacter
# DC         Directional Coupler
# DP         Duplexer
# DL         Delay Line
# DS         Digital Display; LED Lamp
# E            Miscellaneous Electrical Part
# F            Fuse
# FB          Ferrite
# FD         Fiducial
# FL          Filter
# G           Generator
# HW        Hardware
# HY         Circulator
# I or ICT In Circuit Test Point
# J            Jack Connector
# JP          Configuration Jumper
# K           Relay
# L            Coil; Inductor
# LS          Loud Speaker/Buzzer
# M           Motor
# MG        Motor-Generator
# MH        Mounting Hole
# MK        Microphone
# MP         Mechanical Part
# P            Plug Type Connector
# PS          Power Supply
# Q           Transistor
# R            Resistor
# RN         Resistor Network
# RT         Thermistor
# S            Switch
# T            Transformer
# TB         Terminal Block
# TC         Thermocouple
# TP          Test Point
# U            Tuner
# U            Integrated Circuit
# V            Electron Tube
# VR         Voltage Regulator
# W           Cable Transmission
# X            Sub-circuit
# Y            Crystal or Oscillator
# Z            Ref Des Suppressed

set_default_tool(KICAD)
lib_search_paths[KICAD] = [
    os.path.abspath('lib/65xx_Library/KiCad'),
    os.path.abspath('lib/kicad-libs'),
    os.path.abspath('lib/KiCad-Schematic-Symbol-Libraries'),
    os.path.abspath('lib/kicad-symbols'),
]


# local parts
local = SchLib(name='local')

# LD112 linear regulator part
ldl112 = Part(name='LDL112_SO8', tool=SKIDL, dest=TEMPLATE)
ldl112.ref_prefix = 'VR'
ldl112.description = '1.2 A low quiescent current LDO'
ldl112 += Pin(num=1, name='VOUT', func=Pin.PWROUT)
ldl112 += Pin(num=2, name='GND', func=Pin.PWRIN)
ldl112 += Pin(num=3, name='GND', func=Pin.PWRIN)
ldl112 += Pin(num=4, name='VIN', func=Pin.PWRIN)
ldl112 += Pin(num=5, name='EN', func=Pin.INPUT)
ldl112 += Pin(num=6, name='GND', func=Pin.PWRIN)
ldl112 += Pin(num=7, name='GND', func=Pin.PWRIN)
ldl112 += Pin(num=8, name='NC', func=Pin.NOCONNECT)
local += ldl112


# global nets
gnd = Net('GND')
vin = Net('VIN')
supply_3v3 = Net('3v3')
supply_1v2 = Net('1v2')


# 3v3 supply switching regulator + filters
@subcircuit
def reg3v3(vin, vout):
    global gnd
    vreg = Part('Regulator_Linear', 'L7805', value='VXO7803-1000', footprint='TO-220_Vertical')
    vreg.ref_prefix = 'VR'
    inC = Part('Device', 'C', value='10uF/50V', footprint='C_1210_HandSoldering')
    outC = Part('Device', 'C', value='22uF/10V', footprint='C_0805_HandSoldering')
    vreg['IN'] += vin, inC[1]
    vreg['GND'] += gnd, inC[2], outC[2]
    vreg['OUT'] += vout, outC[1]

# 1v2 supply switching regulator + filters
@subcircuit
def reg1v2(vin, vout):
    global gnd
    global local
    vreg = Part(local, 'LDL112_SO8', value='LDL112D12R', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm')
    inC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    outC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    vreg['IN'] += vin, inC[1]
    vreg['GND'] += gnd
    gnd += inC[2], outC[2]
    vreg['OUT'] += vout, outC[1]
    vreg['EN'] += vin    # tie enable high

reg3v3(vin, supply_3v3)
reg1v2(supply_3v3, supply_1v2)

# crap here
cpu = Part('65xx', 'WD65C816S', footprint='PLCC44')
fpga = Part('Lattice_iCE_FPGA', 'iCE40-HX4K-TQ144', footprint='TQFP-144_20x20mm_Pitch0.5mm')
cpu['VCC'] += supply_3v3

data = Bus('data', 8)

cpu['D[0:7]'] += data
fpga['IOT_[168:177]'] += data


if __name__ == "__main__":
    ERC()
    generate_netlist()
