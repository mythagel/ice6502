#!/usr/bin/python3
from skidl import *
import os
import glob
from parts import *

# could probably solder 0603

# Setup
set_default_tool(KICAD)
lib_search_paths[KICAD] = [
    os.path.abspath('lib/kicad-libs'),
    os.path.abspath('lib/KiCad-Schematic-Symbol-Libraries'),
    os.path.abspath('lib/kicad-symbols'),
]

# global nets
gnd = Net('GND')
gnd.drive = POWER
supply_3v3 = Net('3v3')
supply_1v2 = Net('1v2')

def connGND(pin):
    global gnd
    pin += gnd
def conn3v3(pin):
    global supply_3v3
    pin += supply_3v3
def conn1v2(pin):
    global supply_1v2
    pin += supply_1v2

def testPoint(net, name, ref):
    tp = Part('Connector_Generic', 'Conn_01x01', ref_prefix='TP', value=name, footprint='Test_Point_Pad_d1.5mm', ref=ref)
    tp[1] += net

# 3v3 supply switching regulator + filters
def reg3v3(vin, vout, ref):
    vreg = Part('Regulator_Linear', 'L7805', value='VXO7803-1000', footprint='TO-220_Vertical', ref=ref[0])
    inC = Part('Device', 'C', value='10uF/50V', footprint='C_1210_HandSoldering', ref=ref[1])
    outC = Part('Device', 'C', value='22uF/10V', footprint='C_0805_HandSoldering', ref=ref[2])
    vreg.IN += vin
    vreg.IN += inC[1]
    vreg.GND += inC[2]
    vreg.GND += outC[2]
    connGND(vreg.GND)
    vreg.OUT += outC[1]
    if vout:
        vreg.OUT += vout

# 1v2 supply switching regulator + filters
def reg1v2(vin, vout, ref):
    global local
    vreg = Part(local, 'LDL112_SO8', value='LDL112D12R', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm', ref=ref[0])
    inC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering', ref=ref[1])
    outC = Part('Device', 'C', value='1uF', footprint='C_0805_HandSoldering', ref=ref[2])
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
    VIN_Conn = Part('Connector_Generic', 'Conn_01x01', value='VIN', footprint='Pin_d1.0mm_L10.0mm', ref=4)
    VIN_Conn[1] += vin
    GND_Conn = Part('Connector_Generic', 'Conn_01x01', value='GND', footprint='Pin_d1.0mm_L10.0mm', ref=5)
    connGND(GND_Conn[1])

    reg3v3(vin, supply_3v3, [2, 8, 9])
    reg1v2(supply_3v3, supply_1v2, [1, 10, 11])

    testPoint(supply_3v3, '3v3', 6)
    testPoint(supply_1v2, '1v2', 7)
    testPoint(gnd, 'GND', 8)

# TODO similar func for decouping caps
def add0805Pullup(vcc, pin, value, ref):
    pullup = Part('Device', 'R', value=value, footprint='R_0805_HandSoldering', ref=ref)
    if vcc:
        vcc += pullup[1]
    pin += pullup[2]

def add0805Filter(vcc, gnd, value, ref):
    f = Part('Device', 'C', value=value, footprint='C_0805_HandSoldering', ref=ref)
    if vcc:
        vcc += f[1]
    gnd += f[2]

def pllFilter(vccpll, gndpll, ref):
    r = Part('Device', 'R', value='100Ohm', footprint='R_0805_HandSoldering', ref=ref[0])
    lf = Part('Device', 'C', value='10uF', footprint='C_0805_HandSoldering', ref=ref[1])
    hf = Part('Device', 'C', value='100nF', footprint='C_0805_HandSoldering', ref=ref[2])

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
    fpga = Part('Lattice_iCE_FPGA', 'iCE40-HX4K-TQ144', footprint='TQFP-144_20x20mm_Pitch0.5mm', ref='U0')

    # TODO supplies and filters
    CRESET_B = Net('~CRESET')
    CDONE = Net('CDONE')
    fpga.CRESET_B += CRESET_B
    fpga.CDONE += CDONE
    add0805Pullup(fpga['VCCIO_2'], fpga.CRESET_B, '10KOhm', 1)
    add0805Pullup(fpga['VCCIO_2'], fpga.CDONE, '2.2KOhm', 2)

    connGND(fpga['GND[9]'])
    conn3v3(fpga['VCCIO'])
    conn1v2(fpga['VCC[4]'])

    pllFilter(fpga.VCCPLL0, fpga.GNDPLL0, [3, 1, 2])
    pllFilter(fpga.VCCPLL1, fpga.GNDPLL1, [4, 3, 4])

    # Other boards connect to 3v3 via schottky with 80mv drop (ref. icestick), but
    # not using NVCM in this design, DS says max of 3.46 for master SPI conf
    conn3v3(fpga['VPP_2V5'])

    # Must be left floating...in applications
    fpga['VPP_FAST'] += NC

    return fpga

@subcircuit
def configEeprom(fpga):
    eeprom = Part('Memory_EEPROM', '25LCxxx', value='AT25SF041-SSHD-B', footprint='SOIC-8_3.9x4.9mm_Pitch1.27mm',
            ref='U1')

    SCK = Net('SCK')
    MOSI = Net('MOSI')
    MISO = Net('MISO')
    CS = Net('CS')

    fpga.IOB_107_SCK += eeprom.SCK, SCK
    fpga.IOB_105_SDO += eeprom.MOSI, MOSI
    fpga.IOB_106_SDI += eeprom.MISO, MISO

    fpga.IOB_108_SS += eeprom['~CS'], CS
    add0805Pullup(fpga.VCC_SPI, fpga.IOB_108_SS, '10KOhm', 5)

    # tie WP/HOLD high
    WPB = Net('~WP')
    eeprom['~WP'] += WPB
    add0805Pullup(eeprom.VCC, eeprom['~WP'], '10KOhm', 6)

    HOLDB = Net('~HOLD')
    eeprom['~HOLD'] += HOLDB
    add0805Pullup(eeprom.VCC, eeprom['~HOLD'], '10KOhm', 7)

    eeprom.VCC += fpga.VCC_SPI
    connGND(eeprom.GND)

    add0805Filter(eeprom.VCC, eeprom.GND, '100nF', 5)

@subcircuit
def programmingHeader(fpga):
    hdr = Part('Connector_Generic', 'Conn_02x04_Odd_Even', value='Programming Header',
            footprint='Pin_Header_Straight_2x04_Pitch2.54mm', ref=3)
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
    led[2] += pin

    r = Part('Device', 'R', value='2.2KOhm', footprint='R_0805_HandSoldering')
    led[1] += r[1]
    connGND(r[2])

@subcircuit
def ledPeripheral(clk, sdi, le, oe, ref):
    drv = Part(local, 'STP16CP05', footprint='TSSOP-24_4.4x7.8mm_Pitch0.65mm', ref=ref[0])
    # 2KOhm = ~15ma
    r = Part('Device', 'R', value='2KOhm', footprint='R_0805_HandSoldering', ref=ref[1])

    drv.CLK += Net('CLK'), clk
    drv.SDI += Net('SDI'), sdi
    drv.LE += Net('LE'), le
    drv['~OE'] += Net('~OE'), oe
    connGND(drv.GND)
    conn3v3(drv.Vdd)
    drv.SDO += NC
    drv['R-EXT'] += r[1]
    connGND(r[2])
    for i in range(0, 15):
        led = Part(local, 'LED', footprint='LED_0805_HandSoldering', ref=ref[2+i])
        led[1] += drv['OUT%d' % i]
        conn3v3(led[2])

rwb = Net('r/~w')     # high = read, low = write
phi2 = Net('phi2')
dataBus = Bus('data', 8)
addressBus = Bus('addr_b', 19)    # decoded by fpga



fpga = makeFPGA()

# fpga configuration / programming
conn3v3(fpga.VCC_SPI)
configEeprom(fpga)
programmingHeader(fpga)

IOL = sorted(fpga['IOL_'], reverse=False, key=lambda pin: int(pin.num))
IOR = sorted(fpga['IOR_'], reverse=False, key=lambda pin: int(pin.num))
IOT = sorted(fpga['IOT_'], reverse=False, key=lambda pin: int(pin.num))

cpuDataBus = Bus('data_c', 8)    # decoded by fpga
cpuAddrBus = Bus('addr_c', 16)    # decoded by fpga

cpuAddrBus[12:15] += [IOT.pop() for _ in range(0,4)]
cpuDataBus[7:0] += [IOT.pop() for _ in range(0,8)]
cpuAddrBus[11:0] += [IOL.pop(0) for _ in range(0,12)]

# Decoded address and data bus
addressBus += [IOR.pop(0) for _ in range(0,19)]
dataBus += [IOR.pop(0) for _ in range(0,8)]

xo = Part('Oscillator', 'ASE-xxxMHz', footprint='Oscillator_SMD_Abracon_ASE-4pin_3.2x2.5mm_HandSoldering', ref=3)
conn3v3(xo.EN)
conn3v3(xo.Vdd)
connGND(xo.GND)
xo.OUT += fpga.IOB_96
add0805Filter(xo.Vdd, xo.GND, '10nF', 6)

#fpga['IOT_206', 'IOT_212', 'IOT_213', 'IOT_214', 'IOT_215', 'IOT_216', 'IOT_217', 'IOT_219'] += dataBus
# NOTE: downstream address lines (24bit); bank address from dataBus while PHI2 is low
#fpga phi2
#fpga rwb

#TODO function to connect bus device
# common bus pins: addr[0:23], data[0:8], RWB, PHI2

ledPeripheral(IOL.pop(0), IOL.pop(0), IOL.pop(0), IOL.pop(0), [4, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    16])

cpu = Part(local, 'W65C816S_PLCC', footprint='PLCC44', ref=5)
conn3v3(cpu['VDD'])
connGND(cpu['VSS'])

cpu.E += NC
cpu.MX += NC
cpu.MLB += NC

cpu['D[0:7]'] += cpuDataBus
cpu['A[0:15]'] += cpuAddrBus

RDY = Net('RDY')
cpu.RDY += RDY
add0805Pullup(supply_3v3, cpu.RDY, '3.3KOhm', 9)
testPoint(cpu.RDY, 'RDY', 1)

RESB = Net('~RES')
cpu.RESB += RESB
add0805Pullup(supply_3v3, cpu.RESB, '2.2KOhm', 10)
testPoint(cpu.RESB, '~RES', 2)


#cpu.RWB += fpga
#cpu.PHI2 += fpga

VDA = Net('VDA')
cpu.VDA += VDA
cpu.VDA += IOT.pop()

# Vector pull - know if a vector address is being read
VPB = Net('~VP')
cpu.VPB += VPB
cpu.VPB += IOL.pop(0)

# VPA/VDA - either high = bus address is valid
VPA = Net('VPA')
cpu.VPA += VPA
cpu.VPA += IOL.pop(0)

ABORTB = Net('~ABORT')
cpu.ABORTB += ABORTB
cpu.ABORTB += IOL.pop(0)


# TODO connect BE to fpga or tie high?
#cpu.BE += fpga
#add0805Pullup(supply_3v3, cpu.BE, '3.3KOhm')


# IRQ design - all individually routed to fpga?
#cpu.IRQB += fpga

#cpu.NMIB += fpga

@subcircuit
def RAM():
    pass

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
    acia.ref = "U3"
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
