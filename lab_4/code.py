# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example scans for any BLE advertisements and prints one advertisement and one scan response
# from every device found. This scan is more detailed than the simple test because it includes
# specialty advertising types.

from adafruit_ble import BLERadio

from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()
# By providing Advertisement as well we include everything, not just specific advertisements.
for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):
    addr = advertisement.address
    if advertisement.scan_response and addr not in scan_responses:
        scan_responses.add(addr)
    elif not advertisement.scan_response and addr not in found:
        found.add(addr)
    else:
        continue
    print(addr, advertisement)
    print("\t" + repr(advertisement))
    print()

print("scan done")





#from adafruit_ble import BLERadio
#from adafruit_ble.advertising import Advertisement
#from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
#
#print("starting scan")
#
#results = BLERadio.start_scan(ProvideServicesAdvertisement, Advertisement)
#print("scan results:")
#print(results)
#print("itemized list:")
#for advertisement in results:
#    print(advertisement)
#    #print(advertisement.short_name, advertisement.complete_name)
#
#print("scan complete")
#
