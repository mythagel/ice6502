#!/usr/bin/python3
from skidl import *

# local parts
local = SchLib(name='local')

led = Part(name='LED', tool=SKIDL, dest=TEMPLATE)
led.ref_prefix = 'LED'
led.description = 'Generic LED'
led += Pin(num=1, name='1', func=Pin.PASSIVE)
led += Pin(num=2, name='2', func=Pin.PASSIVE)
local += led

# LD112 linear regulator
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
local += W65C816S

# LED Driver
stp16 = Part(name='STP16CP05', tool=SKIDL, dest=TEMPLATE)
stp16.ref_prefix = 'U'
stp16.description = '16-bit constant current LED sink driver'
stp16 += Pin(num=1, name='GND', func=Pin.PWRIN)
stp16 += Pin(num=2, name='SDI', func=Pin.INPUT)
stp16 += Pin(num=3, name='CLK', func=Pin.INPUT)
stp16 += Pin(num=4, name='LE/DM1', func=Pin.INPUT)
stp16 += Pin(num=5, name='OUT0', func=Pin.PWROUT)
stp16 += Pin(num=6, name='OUT1', func=Pin.PWROUT)
stp16 += Pin(num=7, name='OUT2', func=Pin.PWROUT)
stp16 += Pin(num=8, name='OUT3', func=Pin.PWROUT)
stp16 += Pin(num=9, name='OUT4', func=Pin.PWROUT)
stp16 += Pin(num=10, name='OUT5', func=Pin.PWROUT)
stp16 += Pin(num=11, name='OUT6', func=Pin.PWROUT)
stp16 += Pin(num=12, name='OUT7', func=Pin.PWROUT)
stp16 += Pin(num=13, name='OUT8', func=Pin.PWROUT)
stp16 += Pin(num=14, name='OUT9', func=Pin.PWROUT)
stp16 += Pin(num=15, name='OUT10', func=Pin.PWROUT)
stp16 += Pin(num=16, name='OUT11', func=Pin.PWROUT)
stp16 += Pin(num=17, name='OUT12', func=Pin.PWROUT)
stp16 += Pin(num=18, name='OUT13', func=Pin.PWROUT)
stp16 += Pin(num=19, name='OUT14', func=Pin.PWROUT)
stp16 += Pin(num=20, name='OUT15', func=Pin.PWROUT)
stp16 += Pin(num=21, name='~OE/DM2', func=Pin.INPUT)
stp16 += Pin(num=22, name='SDO', func=Pin.OUTPUT)
stp16 += Pin(num=23, name='R-EXT', func=Pin.INPUT)
stp16 += Pin(num=24, name='Vdd', func=Pin.PWRIN)
local += stp16

is62wvs = Part(name='IS62WVS_SOIC', tool=SKIDL, dest=TEMPLATE)
is62wvs.ref_prefix = 'U'
is62wvs.description = 'Fast serial SRAM'
is62wvs += Pin(num=1, name='~CS', func=Pin.INPUT)
is62wvs += Pin(num=2, name='SIO1', func=Pin.BIDIR)
is62wvs += Pin(num=3, name='SIO2', func=Pin.BIDIR)
is62wvs += Pin(num=4, name='VSS', func=Pin.PWRIN)
is62wvs += Pin(num=5, name='SIO0', func=Pin.BIDIR)
is62wvs += Pin(num=6, name='SCK', func=Pin.INPUT)
is62wvs += Pin(num=7, name='SIO3', func=Pin.BIDIR)
is62wvs += Pin(num=8, name='VDD', func=Pin.PWRIN)
local += is62wvs
