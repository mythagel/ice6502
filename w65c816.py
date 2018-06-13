#!/usr/bin/python3
from skidl import *
import os
import glob
from parts import *

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

# Setup
set_default_tool(KICAD)
lib_search_paths[KICAD] = [
    os.path.abspath('lib/kicad-libs'),
    os.path.abspath('lib/KiCad-Schematic-Symbol-Libraries'),
    os.path.abspath('lib/kicad-symbols'),
]

# global nets
gnd = Net('GND')
vin = Net('VIN')
gnd.drive = POWER
vin.drive = POWER

supply_3v3 = Net('3v3')
#supply_3v3.drive = POWER

supply_1v2 = Net('1v2')
#supply_1v2.drive = POWER

VIN_Conn = Part('Connector_Generic', 'Conn_01x01', value='VIN', footprint='Pin_d1.0mm_L10.0mm')
VIN_Conn[1] += vin
GND_Conn = Part('Connector_Generic', 'Conn_01x01', value='GND', footprint='Pin_d1.0mm_L10.0mm')
GND_Conn[1] += gnd

@subcircuit
def testPoints():
    global supply_3v3
    global supply_1v2
    global gnd
    tp3v3 = Part('Connector_Generic', 'Conn_01x01', ref_prefix='TP', value='3v3', footprint='Test_Point_Pad_d1.5mm')
    tp3v3[1] += supply_3v3
    tp1v2 = Part('Connector_Generic', 'Conn_01x01', ref_prefix='TP', value='1v2', footprint='Test_Point_Pad_d1.5mm')
    tp1v2[1] += supply_1v2
    tpgnd = Part('Connector_Generic', 'Conn_01x01', ref_prefix='TP', value='GND', footprint='Test_Point_Pad_d1.5mm')
    tpgnd[1] += gnd
    # other logic test points

testPoints()

# 3v3 supply switching regulator + filters
@subcircuit
def reg3v3(vin, vout):
    global gnd
    vreg = Part('Regulator_Linear', 'L7805', value='VXO7803-1000', footprint='TO-220_Vertical')
    vreg.ref_prefix = 'VR'
    inC = Part('Device', 'C', value='10uF/50V', footprint='C_1210_HandSoldering')
    outC = Part('Device', 'C', value='22uF/10V', footprint='C_0805_HandSoldering')
    vreg.IN += vin, inC[1]
    vreg.GND += gnd, inC[2], outC[2]
    vreg.OUT += vout, outC[1]

# 1v2 supply switching regulator + filters
@subcircuit
def reg1v2(vin, vout):
    global gnd
    global local
    vreg = Part(local, 'LDL112_SO8', value='LDL112D12R', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm')
    inC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    outC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    vreg.VIN += vin, inC[1]
    vreg['GND'] += gnd
    gnd += inC[2], outC[2]
    vreg.VOUT += vout, outC[1]
    vreg.EN += vin    # tie enable high

reg3v3(vin, supply_3v3)
reg1v2(supply_3v3, supply_1v2)

@subcircuit
def add0805Pullup(vcc, pin, value):
    pullup = Part('Device', 'R', value=value, footprint='C_0805_HandSoldering')
    vcc += pullup[1]
    pin += pullup[2]

@subcircuit
def pllFilter(vccpll, gndpll):
    global supply_1v2
    r = Part('Device', 'R', value='100Ohm', footprint='C_0805_HandSoldering')
    lf = Part('Device', 'C', value='10uF', footprint='C_0805_HandSoldering')
    hf = Part('Device', 'C', value='100nF', footprint='C_0805_HandSoldering')

    a = Net()
    a += vccpll
    a.drive = POWER

    b = Net()
    b += gndpll
    b.drive = POWER

    r[1] += supply_1v2
    vccpll += r[2]

    r[2] += lf[1]
    r[2] += hf[1]
    lf[2] += gndpll
    hf[2] += gndpll

#fpga
@subcircuit
def makeFPGA():
    global gnd
    global supply_3v3
    global supply_1v2
    fpga = Part('Lattice_iCE_FPGA', 'iCE40-HX4K-TQ144', footprint='TQFP-144_20x20mm_Pitch0.5mm')

    # TODO supplies and filters
    add0805Pullup(fpga['VCCIO_2'], fpga.CRESET_B, '10KOhm')
    add0805Pullup(fpga['VCCIO_2'], fpga.CDONE, '2.2KOhm')

    fpga['GND[9]'] += gnd
    fpga['VCCIO'] += supply_3v3
    fpga['VCC[4]'] += supply_1v2

    pllFilter(fpga.VCCPLL0, fpga.GNDPLL0)
    pllFilter(fpga.VCCPLL1, fpga.GNDPLL1)

    # Other boards connect to 3v3 via schottky with 80mv drop (ref. icestick), but
    # not using NVCM in this design, DS says max of 3.46 for master SPI conf
    fpga['VPP_2V5'] += supply_3v3

    # Must be left floating...in applications
    fpga['VPP_FAST'] += NC

    return fpga

@subcircuit
def configEeprom(fpga):
    global gnd

    eeprom = Part('Memory_EEPROM', '25LCxxx', value='AT25SF041-SSHD-B', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm')
    fpga.IOB_107_SCK += eeprom.SCK
    fpga.IOB_105_SDO += eeprom.MOSI
    fpga.IOB_106_SDI += eeprom.MISO

    fpga.IOB_108_SS += eeprom['~CS']
    add0805Pullup(fpga.VCC_SPI, fpga.IOB_108_SS, '10KOhm')

    # tie WP/HOLD high
    WP_up = Part('Device', 'R', value='10KOhm', footprint='C_0805_HandSoldering')
    eeprom['~WP'] += WP_up[1]
    eeprom['~HOLD'] += WP_up[1]
    eeprom.VCC += WP_up[2]

    eeprom.VCC += fpga.VCC_SPI
    eeprom.GND += gnd
    C = Part('Device', 'C', value='100nF', footprint='C_0603_HandSoldering')
    C[1] += eeprom.VCC
    C[2] += eeprom.GND

@subcircuit
def programmingHeader(fpga):
    hdr = Part('Connector_Generic', 'Conn_02x04_Odd_Even', value='Programming Header', footprint='Pin_Header_Straight_2x04_Pitch2.54mm')
    hdr[1] += fpga.VCC_SPI
    hdr[2] += gnd
    hdr[3] += fpga.CDONE
    hdr[4] += fpga.CRESET_B
    hdr[5] += fpga.IOB_105_SDO
    hdr[6] += fpga.IOB_106_SDI
    hdr[7] += fpga.IOB_107_SCK
    hdr[8] += fpga.IOB_108_SS

fpga = makeFPGA()

dataBus = Bus('data', 8)
addressBus = Bus('addr', 16)

sram = Part(local, 'IS61WV', value='IS61WV5128EDBLL-10TLI', footprint='TSOP-II-44_10.16x18.42_Pitch0.8mm')
sram['Vdd'] += supply_3v3
sram['GND'] += gnd

sram['IO[0:7]'] += dataBus
sram['A[0:15]'] += addressBus
sram['A[16:18]'] += fpga['IOR_161', 'IOR_164', 'IOR_165']
sram.CE_B += fpga.IOB_56
sram.WE_B += fpga.IOB_57
sram.OE_B += fpga.IOB_61

# Configuration / Programming
fpga.VCC_SPI += supply_3v3
configEeprom(fpga)
programmingHeader(fpga)

# crap here
cpu = Part(local, 'W65C816S_PLCC', footprint='PLCC44')
cpu['VDD'] += supply_3v3
cpu['VSS'] += gnd
cpu['D[0:7]'] += dataBus

# NOTE: CPU address lines go to different bank
cpu['A[15:0]'] += fpga['IOT_168', 'IOT_169', 'IOT_170', 'IOT_171', 'IOT_172', 'IOT_173', 'IOT_174', 'IOT_177', 'IOT_178', 'IOT_179', 'IOT_181', 'IOT_190', 'IOT_191', 'IOT_192', 'IOT_197_GBIN1', 'IOT_198_GBIN0']

fpga['IOR_109', 'IOR_110', 'IOR_111', 'IOR_112', 'IOR_114', 'IOR_115', 'IOR_116', 'IOR_117'] += dataBus
fpga['IOR_118', 'IOR_119', 'IOR_120', 'IOR_128', 'IOR_136', 'IOR_137', 'IOR_138', 'IOR_139', 'IOR_140_GBIN3',
        'IOR_141_GBIN2', 'IOR_144', 'IOR_146', 'IOR_147', 'IOR_148', 'IOR_152', 'IOR_160'] += addressBus[15:0]

via = Part(local, 'W65C22S_PLCC', footprint='PLCC44')
via['VDD'] += supply_3v3
via['VSS'] += gnd
via['D[0:7]'] += dataBus
via['RS[0:3]'] += addressBus[0:3]

acia = Part(local, 'W65C51N_PLCC', footprint='PLCC28')
acia['VDD'] += supply_3v3
acia['VSS'] += gnd
acia['D[0:7]'] += dataBus
acia['RS[0:1]'] += addressBus[0:1]

if sys.argv[1] == 'generate':
    ERC()
    generate_netlist()
