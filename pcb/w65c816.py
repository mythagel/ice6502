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


# could probably solder 0603

# Setup
set_default_tool(KICAD)
lib_search_paths[KICAD] = [
    os.path.abspath('lib/kicad-libs'),
    os.path.abspath('lib/KiCad-Schematic-Symbol-Libraries'),
    os.path.abspath('lib/kicad-symbols'),
]

# Generating the netlist without power nets makes arranging the components
# easier when laying out the pcb as related components are easily grouped.
# Then turn them back on and route power and ground
distributePower = False

# global nets
if distributePower:
    gnd = Net('GND')
    gnd.drive = POWER
    supply_3v3 = Net('3v3')
    supply_1v2 = Net('1v2')
else:
    gnd = None
    supply_3v3 = None
    supply_1v2 = None

def connGND(pin):
    global gnd
    if distributePower:
        pin += gnd
def conn3v3(pin):
    global supply_3v3
    if distributePower:
        pin += supply_3v3
def conn1v2(pin):
    global supply_1v2
    if distributePower:
        pin += supply_1v2

@subcircuit
def testPoint(net, name):
    tp = Part('Connector_Generic', 'Conn_01x01', ref_prefix='TP', value=name, footprint='Test_Point_Pad_d1.5mm')
    tp[1] += net

# 3v3 supply switching regulator + filters
@subcircuit
def reg3v3(vin, vout):
    vreg = Part('Regulator_Linear', 'L7805', value='VXO7803-1000', footprint='TO-220_Vertical')
    vreg.ref_prefix = 'VR'
    inC = Part('Device', 'C', value='10uF/50V', footprint='C_1210_HandSoldering')
    outC = Part('Device', 'C', value='22uF/10V', footprint='C_0805_HandSoldering')
    vreg.IN += vin
    vreg.IN += inC[1]
    vreg.GND += inC[2]
    vreg.GND += outC[2]
    connGND(vreg.GND)
    vreg.OUT += outC[1]
    if vout:
        vreg.OUT += vout

# 1v2 supply switching regulator + filters
@subcircuit
def reg1v2(vin, vout):
    global local
    vreg = Part(local, 'LDL112_SO8', value='LDL112D12R', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm')
    inC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    outC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering')
    vreg.VIN += inC[1]
    if vin:
        vreg.VIN += vin
    connGND(vreg['GND'])
    vreg['GND'] += inC[2]
    vreg['GND'] += outC[2]
    vreg.VOUT += outC[1]
    if vout:
        vreg.VOUT += vout
    vreg.EN += vreg.VIN    # tie enable high

@subcircuit
def powerSupply():
    vin = Net('VIN')
    vin.drive = POWER
    VIN_Conn = Part('Connector_Generic', 'Conn_01x01', value='VIN', footprint='Pin_d1.0mm_L10.0mm')
    VIN_Conn[1] += vin
    GND_Conn = Part('Connector_Generic', 'Conn_01x01', value='GND', footprint='Pin_d1.0mm_L10.0mm')
    connGND(GND_Conn[1])

    reg3v3(vin, supply_3v3)
    reg1v2(supply_3v3, supply_1v2)

    if distributePower:
        testPoint(supply_3v3, '3v3')
        testPoint(supply_1v2, '1v2')
        testPoint(gnd, 'GND')

# TODO similar func for decouping caps
@subcircuit
def add0805Pullup(vcc, pin, value):
    pullup = Part('Device', 'R', value=value, footprint='R_0805_HandSoldering')
    if vcc:
        vcc += pullup[1]
    pin += pullup[2]

@subcircuit
def add0805Filter(vcc, gnd, value):
    f = Part('Device', 'C', value=value, footprint='C_0805_HandSoldering')
    if vcc:
        vcc += f[1]
    gnd += f[2]

@subcircuit
def pllFilter(vccpll, gndpll):
    r = Part('Device', 'R', value='100Ohm', footprint='R_0805_HandSoldering')
    lf = Part('Device', 'C', value='10uF', footprint='C_0805_HandSoldering')
    hf = Part('Device', 'C', value='100nF', footprint='C_0805_HandSoldering')

    a = Net('PLLVCC')
    a += vccpll
    a.drive = POWER

    b = Net('PLLGND')
    b += gndpll
    b.drive = POWER

    conn1v2(r[1])
    vccpll += r[2]

    r[2] += lf[1]
    r[2] += hf[1]
    lf[2] += gndpll
    hf[2] += gndpll

@subcircuit
def makeFPGA():
    fpga = Part('Lattice_iCE_FPGA', 'iCE40-HX4K-TQ144', footprint='TQFP-144_20x20mm_Pitch0.5mm')
    fpga.ref = "U0"

    # TODO supplies and filters
    add0805Pullup(fpga['VCCIO_2'], fpga.CRESET_B, '10KOhm')
    add0805Pullup(fpga['VCCIO_2'], fpga.CDONE, '2.2KOhm')

    connGND(fpga['GND[9]'])
    conn3v3(fpga['VCCIO'])
    conn1v2(fpga['VCC[4]'])

    pllFilter(fpga.VCCPLL0, fpga.GNDPLL0)
    pllFilter(fpga.VCCPLL1, fpga.GNDPLL1)

    # Other boards connect to 3v3 via schottky with 80mv drop (ref. icestick), but
    # not using NVCM in this design, DS says max of 3.46 for master SPI conf
    conn3v3(fpga['VPP_2V5'])

    # Must be left floating...in applications
    fpga['VPP_FAST'] += NC

    return fpga

@subcircuit
def configEeprom(fpga):
    eeprom = Part('Memory_EEPROM', '25LCxxx', value='AT25SF041-SSHD-B', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm')
    fpga.IOB_107_SCK += eeprom.SCK
    fpga.IOB_105_SDO += eeprom.MOSI
    fpga.IOB_106_SDI += eeprom.MISO

    fpga.IOB_108_SS += eeprom['~CS']
    add0805Pullup(fpga.VCC_SPI, fpga.IOB_108_SS, '10KOhm')

    # tie WP/HOLD high
    WP_up = Part('Device', 'R', value='10KOhm', footprint='R_0805_HandSoldering')
    eeprom['~WP'] += WP_up[1]
    eeprom['~HOLD'] += WP_up[1]
    eeprom.VCC += WP_up[2]

    eeprom.VCC += fpga.VCC_SPI
    connGND(eeprom.GND)

    add0805Filter(eeprom.VCC, eeprom.GND, '100nF')

@subcircuit
def programmingHeader(fpga):
    hdr = Part('Connector_Generic', 'Conn_02x04_Odd_Even', value='Programming Header', footprint='Pin_Header_Straight_2x04_Pitch2.54mm')
    hdr[1] += fpga.VCC_SPI
    connGND(hdr[2])
    hdr[3] += fpga.CDONE
    hdr[4] += fpga.CRESET_B
    hdr[5] += fpga.IOB_105_SDO
    hdr[6] += fpga.IOB_106_SDI
    hdr[7] += fpga.IOB_107_SCK
    hdr[8] += fpga.IOB_108_SS

@subcircuit
def led(pin):
    global local
    led = Part(local, 'LED', footprint='LED_0805_HandSoldering')
    r = Part('Device', 'R', value='2.2KOhm', footprint='R_0805_HandSoldering')
    led[2] += pin
    led[1] += r[1]
    connGND(r[2])

@subcircuit
def ledPeripheral(fpga):
    led(fpga.IOB_63)
    led(fpga.IOB_64)
    led(fpga.IOB_71)
    led(fpga.IOB_72)
    led(fpga.IOB_73)
    led(fpga.IOB_79)
    led(fpga.IOB_80)
    led(fpga.IOB_81_GBIN5)

dataBus = Bus('data', 8)
rwb = Bus('r/wb', 1)     # high = read, low = write
phi2 = Bus('phi2', 1)
addressBus = Bus('addr_b', 24)    # decoded by fpga



fpga = makeFPGA()

# fpga configuration / programming
conn3v3(fpga.VCC_SPI)
configEeprom(fpga)
programmingHeader(fpga)

IOL = sorted(fpga['IOL_'], reverse=True, key=lambda pin: int(pin.num))
cpuAddrBus = Bus('addr_c', 16)    # decoded by fpga
cpuAddrBus += IOL[0:16]
dataBus[7:0] += IOL[17:25]


xo = Part('Oscillator', 'VC-81', footprint='Oscillator_DIP-8')
conn3v3(xo.Vcontrol)
conn3v3(xo.Vcc)
connGND(xo.GND)
xo.OUT += fpga.IOB_96
add0805Filter(xo.Vcc, xo.GND, '10nF')

#fpga['IOT_206', 'IOT_212', 'IOT_213', 'IOT_214', 'IOT_215', 'IOT_216', 'IOT_217', 'IOT_219'] += dataBus
# NOTE: downstream address lines (24bit); bank address from dataBus while PHI2 is low
#fpga phi2
#fpga rwb

#TODO function to connect bus device
# common bus pins: addr[0:23], data[0:8], RWB, PHI2

ledPeripheral(fpga)

cpu = Part(local, 'W65C816S_PLCC', footprint='PLCC44')
cpu.ref = "U1"
conn3v3(cpu['VDD'])
connGND(cpu['VSS'])

cpu.E += NC
cpu.MX += NC

cpu['D[0:7]'] += dataBus
# NOTE: upstream address lines (16bit)
cpu['A[0:15]'] += cpuAddrBus
#cpu.RWB += fpga
#cpu.PHI2 += fpga

add0805Pullup(supply_3v3, cpu.RDY, '3.3KOhm')
testPoint(cpu.RDY, 'RDY')

add0805Pullup(supply_3v3, cpu.RESB, '2.2KOhm')
testPoint(cpu.RESB, 'RESB')

# Vector pull - know if a vector address is being read
#cpu.VPB += fpga

# VPA/VDA - either high = bus address is value
#cpu.VPA += fpga
#cpu.VDA += fpga

#cpu.ABORTB += fpga
#cpu.BE += fpga

# IRQ design - all individually routed to fpga?
#cpu.IRQB += fpga

#cpu.NMIB += fpga


@subcircuit
def RAM():
    global local
    global dataBus
    global addressBus
    sram = Part(local, 'IS61WV', value='IS61WV5128EDBLL-10TLI', footprint='TSOP-II-44_10.16x18.42_Pitch0.8mm')
    conn3v3(sram['Vdd'])
    connGND(sram['GND'])

    sram['IO[0:7]'] += dataBus
    sram['A[0:18]'] += addressBus[0:18]
    sram.CE_B += fpga.IOB_56
    sram.WE_B += fpga.IOB_57
    sram.OE_B += fpga.IOB_61

@subcircuit
def VIA():
    global local
    global dataBus
    global addressBus
    via = Part(local, 'W65C22S_PLCC', footprint='PLCC44')
    via.ref = "U2"
    conn3v3(via['VDD'])
    connGND(via['VSS'])
    via['D[0:7]'] += dataBus
    via['RS[0:3]'] += addressBus[0:3]
    # IRQ, PHI2, RWB

@subcircuit
def ACIA():
    global local
    global dataBus
    global addressBus
    acia = Part(local, 'W65C51N_PLCC', footprint='PLCC28')
    via.ref = "U3"
    conn3v3(acia['VDD'])
    connGND(acia['VSS'])
    acia['D[0:7]'] += dataBus
    acia['RS[0:1]'] += addressBus[0:1]
    # IRQ, PHI2, RWB

powerSupply()
RAM()
#VIA()
#ACIA()

if sys.argv[1] == 'generate':
    ERC()
    generate_netlist()
