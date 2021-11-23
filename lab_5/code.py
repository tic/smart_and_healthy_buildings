# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example scans for any BLE advertisements and prints one advertisement and one scan response
# from every device found. This scan is more detailed than the simple test because it includes
# specialty advertising types.

from adafruit_ble import BLERadio

from adafruit_ble.advertising import Advertisement, to_hex
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()

DATA_TYPE = 255 # "manufacturer specific"
MANUFACTURER = b'\x4c\x00' # Apple
APPLE_DATA_TYPE = 2 # iBeacon data
ATTENUATION = 0.1 # integer in [2, 6] to adjust for environmental circumstances
CALIBRATION = 1 # value to scale distance measurements

# By providing Advertisement as well we include everything, not just specific advertisements.
for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):

    # get the ad content in bytes
    adbytes = bytes(advertisement)

    # if data type is not 0xff, skip to next ad
    if(adbytes[1] != DATA_TYPE):
        continue

    if(adbytes[2:4] != MANUFACTURER):
        continue

    if(adbytes[4] != APPLE_DATA_TYPE):
        continue

    bg = ("{0:0{1}x}".format(b, 2) for b in advertisement.address.address_bytes)
    bytes_list = list(bg)
    bytes_list.reverse()
    MACAddress = ':'.join(bytes_list)
    TXPower = adbytes[29]
    RSSI = advertisement.rssi

    # exponent = float(RSSI - TXPower) / float(10*ATTENUATION)
    # estimatedDistance = (10**exponent) * CALIBRATION

    raw_exponent = float(RSSI - TXPower) / float(10*ATTENUATION)
    exponent = (raw_exponent + 2) / -15
    estimatedDistance = (2.718 ** exponent) * CALIBRATION

    # look for specific calibration sensors
    # if 'e7' in MACAddress or '74' in MACAddress or '69' in MACAddress:
    print(MACAddress, TXPower, RSSI, exponent, estimatedDistance)


print("scan done")
