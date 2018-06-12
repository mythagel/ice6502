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

# Setup
set_default_tool(KICAD)
lib_search_paths[KICAD] = [
    os.path.abspath('lib/kicad-libs'),
    os.path.abspath('lib/KiCad-Schematic-Symbol-Libraries'),
    os.path.abspath('lib/kicad-symbols'),
]


# local parts
local = SchLib(name='local')

# LD112 linear regulator
def makeLocalParts(lib):
    ldl112 = Part(name='LDL112_SO8', tool=SKIDL, dest=TEMPLATE)
    ldl112.ref_prefix = 'VR'
    ldl112.description = '1.2 A low quiescent current LDO'
    ldl112 += Pin(num=1, name='VOUT', func=Pin.PWROUT, drive=POWER)
    ldl112 += Pin(num=2, name='GND', func=Pin.PWRIN)
    ldl112 += Pin(num=3, name='GND', func=Pin.PWRIN)
    ldl112 += Pin(num=4, name='VIN', func=Pin.PWRIN)
    ldl112 += Pin(num=5, name='EN', func=Pin.INPUT)
    ldl112 += Pin(num=6, name='GND', func=Pin.PWRIN)
    ldl112 += Pin(num=7, name='GND', func=Pin.PWRIN)
    ldl112 += Pin(num=8, name='NC', func=Pin.NOCONNECT)
    lib += ldl112

    W65C816S = Part(name='W65C816S_PLCC', tool=SKIDL, dest=TEMPLATE)
    W65C816S.ref_prefix = 'U'
    W65C816S.description = 'W65C816S 8/16–bit Microprocessor'
    W65C816S += Pin(num='1', name='VSS', func=Pin.PWRIN)
    W65C816S += Pin(num='2', name='VPB', func=Pin.OUTPUT)
    W65C816S += Pin(num='3', name='RDY', func=Pin.BIDIR)
    W65C816S += Pin(num='4', name='ABORTB', func=Pin.INPUT)
    W65C816S += Pin(num='5', name='IRQB', func=Pin.INPUT)
    W65C816S += Pin(num='6', name='MLB', func=Pin.OUTPUT)
    W65C816S += Pin(num='7', name='NMIB', func=Pin.INPUT)
    W65C816S += Pin(num='8', name='VPA', func=Pin.OUTPUT)
    W65C816S += Pin(num='9', name='VDD', func=Pin.PWRIN)
    W65C816S += Pin(num='10', name='A0', func=Pin.OUTPUT)
    W65C816S += Pin(num='11', name='A1', func=Pin.OUTPUT)
    W65C816S += Pin(num='12', name='NC', func=Pin.NOCONNECT)
    W65C816S += Pin(num='13', name='A2', func=Pin.OUTPUT)
    W65C816S += Pin(num='14', name='A3', func=Pin.OUTPUT)
    W65C816S += Pin(num='15', name='A4', func=Pin.OUTPUT)
    W65C816S += Pin(num='16', name='A5', func=Pin.OUTPUT)
    W65C816S += Pin(num='17', name='A6', func=Pin.OUTPUT)
    W65C816S += Pin(num='18', name='A7', func=Pin.OUTPUT)
    W65C816S += Pin(num='19', name='A8', func=Pin.OUTPUT)
    W65C816S += Pin(num='20', name='A9', func=Pin.OUTPUT)
    W65C816S += Pin(num='21', name='A10', func=Pin.OUTPUT)
    W65C816S += Pin(num='22', name='A11', func=Pin.OUTPUT)
    W65C816S += Pin(num='23', name='VSS', func=Pin.PWRIN)
    W65C816S += Pin(num='24', name='VSS', func=Pin.PWRIN)
    W65C816S += Pin(num='25', name='A12', func=Pin.OUTPUT)
    W65C816S += Pin(num='26', name='A13', func=Pin.OUTPUT)
    W65C816S += Pin(num='27', name='A14', func=Pin.OUTPUT)
    W65C816S += Pin(num='28', name='A15', func=Pin.OUTPUT)
    W65C816S += Pin(num='29', name='D7', func=Pin.TRISTATE)
    W65C816S += Pin(num='30', name='D6', func=Pin.TRISTATE)
    W65C816S += Pin(num='31', name='D5', func=Pin.TRISTATE)
    W65C816S += Pin(num='32', name='D4', func=Pin.TRISTATE)
    W65C816S += Pin(num='33', name='D3', func=Pin.TRISTATE)
    W65C816S += Pin(num='34', name='D2', func=Pin.TRISTATE)
    W65C816S += Pin(num='35', name='D1', func=Pin.TRISTATE)
    W65C816S += Pin(num='36', name='D0', func=Pin.TRISTATE)
    W65C816S += Pin(num='37', name='VDD', func=Pin.PWRIN)
    W65C816S += Pin(num='38', name='RWB', func=Pin.OUTPUT)
    W65C816S += Pin(num='39', name='E', func=Pin.OUTPUT)
    W65C816S += Pin(num='40', name='BE', func=Pin.INPUT)
    W65C816S += Pin(num='41', name='PHI2', func=Pin.INPUT)
    W65C816S += Pin(num='42', name='MX', func=Pin.OUTPUT)
    W65C816S += Pin(num='43', name='VDA', func=Pin.OUTPUT)
    W65C816S += Pin(num='44', name='RESB', func=Pin.INPUT)
    lib += W65C816S

    IS61WV = Part(name='IS61WV', tool=SKIDL, dest=TEMPLATE)
    IS61WV.ref_prefix = 'U'
    IS61WV.description = 'W65C816S 8/16–bit Microprocessor'
    IS61WV += Pin(num='1', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='2', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='3', name='A0', func=Pin.INPUT)
    IS61WV += Pin(num='4', name='A1', func=Pin.INPUT)
    IS61WV += Pin(num='5', name='A2', func=Pin.INPUT)
    IS61WV += Pin(num='6', name='A3', func=Pin.INPUT)
    IS61WV += Pin(num='7', name='A4', func=Pin.INPUT)
    IS61WV += Pin(num='8', name='CE_B', func=Pin.INPUT)
    IS61WV += Pin(num='9', name='IO0', func=Pin.TRISTATE)
    IS61WV += Pin(num='10', name='IO1', func=Pin.TRISTATE)
    IS61WV += Pin(num='11', name='Vdd', func=Pin.PWRIN)
    IS61WV += Pin(num='12', name='GND', func=Pin.PWRIN)
    IS61WV += Pin(num='13', name='IO2', func=Pin.TRISTATE)
    IS61WV += Pin(num='14', name='IO3', func=Pin.TRISTATE)
    IS61WV += Pin(num='15', name='WE_B', func=Pin.INPUT)
    IS61WV += Pin(num='16', name='A5', func=Pin.INPUT)
    IS61WV += Pin(num='17', name='A6', func=Pin.INPUT)
    IS61WV += Pin(num='18', name='A7', func=Pin.INPUT)
    IS61WV += Pin(num='19', name='A8', func=Pin.INPUT)
    IS61WV += Pin(num='20', name='A9', func=Pin.INPUT)
    IS61WV += Pin(num='21', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='22', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='23', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='24', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='25', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='26', name='A10', func=Pin.INPUT)
    IS61WV += Pin(num='27', name='A11', func=Pin.INPUT)
    IS61WV += Pin(num='28', name='A12', func=Pin.INPUT)
    IS61WV += Pin(num='29', name='A13', func=Pin.INPUT)
    IS61WV += Pin(num='30', name='A14', func=Pin.INPUT)
    IS61WV += Pin(num='31', name='IO4', func=Pin.TRISTATE)
    IS61WV += Pin(num='32', name='IO5', func=Pin.TRISTATE)
    IS61WV += Pin(num='33', name='Vdd', func=Pin.PWRIN)
    IS61WV += Pin(num='34', name='GND', func=Pin.PWRIN)
    IS61WV += Pin(num='35', name='IO6', func=Pin.TRISTATE)
    IS61WV += Pin(num='36', name='IO7', func=Pin.TRISTATE)
    IS61WV += Pin(num='37', name='OE_B', func=Pin.INPUT)
    IS61WV += Pin(num='38', name='A15', func=Pin.INPUT)
    IS61WV += Pin(num='39', name='A16', func=Pin.INPUT)
    IS61WV += Pin(num='40', name='A17', func=Pin.INPUT)
    IS61WV += Pin(num='41', name='A18', func=Pin.INPUT)
    IS61WV += Pin(num='42', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='43', name='NC', func=Pin.NOCONNECT)
    IS61WV += Pin(num='44', name='NC', func=Pin.NOCONNECT)
    lib += IS61WV

    W65C22S = Part(name='W65C22S_PLCC', tool=SKIDL, dest=TEMPLATE)
    W65C22S.ref_prefix = 'U'
    W65C22S.description = 'Versatile Interface Adapter (VIA)'
    W65C22S += Pin(num='1', name='VSS', func=Pin.PWRIN)
    W65C22S += Pin(num='2', name='PA0', func=Pin.BIDIR)
    W65C22S += Pin(num='3', name='PA1', func=Pin.BIDIR)
    W65C22S += Pin(num='4', name='PA2', func=Pin.BIDIR)
    W65C22S += Pin(num='5', name='PA3', func=Pin.BIDIR)
    W65C22S += Pin(num='6', name='PA4', func=Pin.BIDIR)
    W65C22S += Pin(num='7', name='PA5', func=Pin.BIDIR)
    W65C22S += Pin(num='8', name='PA6', func=Pin.BIDIR)
    W65C22S += Pin(num='9', name='PA7', func=Pin.BIDIR)
    W65C22S += Pin(num='10', name='PB0', func=Pin.BIDIR)
    W65C22S += Pin(num='11', name='NC', func=Pin.NOCONNECT)
    W65C22S += Pin(num='12', name='PB1', func=Pin.BIDIR)
    W65C22S += Pin(num='13', name='PB2', func=Pin.BIDIR)
    W65C22S += Pin(num='14', name='PB3', func=Pin.BIDIR)
    W65C22S += Pin(num='15', name='PB4', func=Pin.BIDIR)
    W65C22S += Pin(num='16', name='PB5', func=Pin.BIDIR)
    W65C22S += Pin(num='17', name='PB6', func=Pin.BIDIR)
    W65C22S += Pin(num='18', name='PB7', func=Pin.BIDIR)
    W65C22S += Pin(num='19', name='CB1', func=Pin.BIDIR)
    W65C22S += Pin(num='20', name='CB2', func=Pin.BIDIR)
    W65C22S += Pin(num='21', name='VDD', func=Pin.PWRIN)
    W65C22S += Pin(num='22', name='NC', func=Pin.NOCONNECT)
    W65C22S += Pin(num='23', name='IRQB', func=Pin.OUTPUT)
    W65C22S += Pin(num='24', name='RWB', func=Pin.INPUT)
    W65C22S += Pin(num='25', name='CS2B', func=Pin.INPUT)
    W65C22S += Pin(num='26', name='CS1', func=Pin.INPUT)
    W65C22S += Pin(num='27', name='PHI2', func=Pin.INPUT)
    W65C22S += Pin(num='28', name='D7', func=Pin.BIDIR)
    W65C22S += Pin(num='29', name='D6', func=Pin.BIDIR)
    W65C22S += Pin(num='30', name='D5', func=Pin.BIDIR)
    W65C22S += Pin(num='31', name='D4', func=Pin.BIDIR)
    W65C22S += Pin(num='32', name='D3', func=Pin.BIDIR)
    W65C22S += Pin(num='33', name='NC', func=Pin.NOCONNECT)
    W65C22S += Pin(num='34', name='D2', func=Pin.BIDIR)
    W65C22S += Pin(num='35', name='D1', func=Pin.BIDIR)
    W65C22S += Pin(num='36', name='D0', func=Pin.BIDIR)
    W65C22S += Pin(num='37', name='RESB', func=Pin.INPUT)
    W65C22S += Pin(num='38', name='NC', func=Pin.NOCONNECT)
    W65C22S += Pin(num='39', name='RS3', func=Pin.INPUT)
    W65C22S += Pin(num='40', name='RS2', func=Pin.INPUT)
    W65C22S += Pin(num='41', name='RS1', func=Pin.INPUT)
    W65C22S += Pin(num='42', name='RS0', func=Pin.INPUT)
    W65C22S += Pin(num='43', name='CA2', func=Pin.BIDIR)
    W65C22S += Pin(num='44', name='CA1', func=Pin.BIDIR)
    lib += W65C22S

    W65C51N = Part(name='W65C51N_PLCC', tool=SKIDL, dest=TEMPLATE)
    W65C51N.ref_prefix = 'U'
    W65C51N.description = 'Asynchrones Communications Interface Adapter'
    W65C51N += Pin(num='1', name='VSS', func=Pin.PWRIN)
    W65C51N += Pin(num='2', name='CS0', func=Pin.INPUT)
    W65C51N += Pin(num='3', name='CS1B', func=Pin.INPUT)
    W65C51N += Pin(num='4', name='RESB', func=Pin.INPUT)
    W65C51N += Pin(num='5', name='RxC', func=Pin.BIDIR)
    W65C51N += Pin(num='6', name='XTL1', func=Pin.INPUT)
    W65C51N += Pin(num='7', name='XTL0', func=Pin.INPUT)
    W65C51N += Pin(num='8', name='RTSB', func=Pin.OUTPUT)
    W65C51N += Pin(num='9', name='CTSB', func=Pin.INPUT)
    W65C51N += Pin(num='10', name='TxD', func=Pin.OUTPUT)
    W65C51N += Pin(num='11', name='DTRB', func=Pin.OUTPUT)
    W65C51N += Pin(num='12', name='RxD', func=Pin.INPUT)
    W65C51N += Pin(num='13', name='RS0', func=Pin.INPUT)
    W65C51N += Pin(num='14', name='RS1', func=Pin.INPUT)
    W65C51N += Pin(num='15', name='VDD', func=Pin.BIDIR)
    W65C51N += Pin(num='16', name='DCDB', func=Pin.INPUT)
    W65C51N += Pin(num='17', name='DSRB', func=Pin.INPUT)
    W65C51N += Pin(num='18', name='D0', func=Pin.BIDIR)
    W65C51N += Pin(num='19', name='D1', func=Pin.BIDIR)
    W65C51N += Pin(num='20', name='D2', func=Pin.BIDIR)
    W65C51N += Pin(num='21', name='D3', func=Pin.BIDIR)
    W65C51N += Pin(num='22', name='D4', func=Pin.BIDIR)
    W65C51N += Pin(num='23', name='D5', func=Pin.BIDIR)
    W65C51N += Pin(num='24', name='D6', func=Pin.BIDIR)
    W65C51N += Pin(num='25', name='D7', func=Pin.BIDIR)
    W65C51N += Pin(num='26', name='IRQB', func=Pin.OUTPUT)
    W65C51N += Pin(num='27', name='PHI2', func=Pin.INPUT)
    W65C51N += Pin(num='28', name='RWB', func=Pin.INPUT)
    lib += W65C51N

makeLocalParts(local)

# global nets
gnd = Net('GND')
vin = Net('VIN')
supply_3v3 = Net('3v3')
supply_1v2 = Net('1v2')

VIN_Conn = Part('Connector_Generic', 'Conn_01x01', drive=POWER, value='VIN', footprint='Pin_d1.0mm_L10.0mm')
VIN_Conn[1] += vin
GND_Conn = Part('Connector_Generic', 'Conn_01x01', drive=POWER, value='GND', footprint='Pin_d1.0mm_L10.0mm')
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

#fpga
@subcircuit
def makeFPGA():
    global gnd
    fpga = Part('Lattice_iCE_FPGA', 'iCE40-HX4K-TQ144', footprint='TQFP-144_20x20mm_Pitch0.5mm')

    # TODO supplies and filters
    add0805Pullup(fpga['VCCIO_2'], fpga.CRESET_B, '10KOhm')
    add0805Pullup(fpga['VCCIO_2'], fpga.CDONE, '2.2KOhm')

    fpga['GND'] += gnd

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
