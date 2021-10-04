# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut


from adafruit_pn532.i2c import PN532_I2C

# Connexió I2C amb el port SCL de recepció i el SDA de transmissió:
i2c = busio.I2C(board.SCL, board.SDA)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configurem PN532 per a que es pugui comunicar amb les targetes
pn532.SAM_configuration()

#Comencem a escriure per pantalla esperant una lectura
#Va llegint cada 1 segon
#Si no troba cap continua llegint
#Si troba una targeta l'escriu per pantalla, però no s'atura
print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=1)
    print(".")
    
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
