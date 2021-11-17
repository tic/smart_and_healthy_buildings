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


# By providing Advertisement as well we include everything, not just specific advertisements.
for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):
    addr = advertisement.address

    # suppresses repeated advertisement data from devices
    if advertisement.scan_response and addr not in scan_responses:
        scan_responses.add(addr)
    elif not advertisement.scan_response and addr not in found:
        found.add(addr)
    else:
        continue

    # get the ad content in bytes
    adbytes = bytes(advertisement)

    # if data type is not 0xff, skip to next ad
    if(adbytes[1] != DATA_TYPE):
        continue

    if(adbytes[2:4] != MANUFACTURER):
        continue

    if(adbytes[4] != APPLE_DATA_TYPE):
        continue

    MACAddress = ':'.join("{0:0{1}x}".format(b, 2) for b in addr.address_bytes)
    TXPower = adbytes[29]
    RSSI = advertisement.rssi
    print(MACAddress, TXPower, RSSI)

    print()

print("scan done")
