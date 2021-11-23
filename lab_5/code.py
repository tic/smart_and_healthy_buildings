# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example scans for any BLE advertisements and prints one advertisement and one scan response
# from every device found. This scan is more detailed than the simple test because it includes
# specialty advertising types.

from adafruit_ble import BLERadio

from adafruit_ble.advertising import Advertisement, to_hex
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

found = set()
scan_responses = set()
beacon_distances = {}

# variables to control how BLE packets are filtered
DATA_TYPE = 255 # "manufacturer specific"
MANUFACTURER = b'\x4c\x00' # Apple
APPLE_DATA_TYPE = 2 # iBeacon data
ATTENUATION = 0.1 # integer in [2, 6] to adjust for environmental circumstances
CALIBRATION = 1 # value to scale distance measurements

# variables to control how many beacons we need to hear from, and how much we
# need to hear from each beacon, before attempting position triangulation
BEACON_COUNT = 6
BEACON_DIST_COUNT = 6


print("scanning")
ble = BLERadio()
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

    # if this is the first time seeing this beacon, initialize it's list of
    # observed positions
    if MACAddress not in beacon_distances:
        beacons[MACAddress] = []

    # exponent = float(RSSI - TXPower) / float(10*ATTENUATION)
    # estimatedDistance = (10**exponent) * CALIBRATION

    raw_exponent = float(RSSI - TXPower) / float(10*ATTENUATION)
    exponent = (raw_exponent + 2) / -15
    estimatedDistance = (2.718 ** exponent) * CALIBRATION

    # only print debug data for specific calibration sensors
    if 'e7' in MACAddress or '74' in MACAddress or '69' in MACAddress:
        print(MACAddress, TXPower, RSSI, exponent, estimatedDistance)

    # record that we heard from the beacon
    beacon_distances[MACAddress].append(estimatedDistance)

    # keep listening for more beacon advertisements if we haven't heard from
    # enough beacons yet
    found_beacons = len(beacon_distances)
    if found_beacons < BEACON_COUNT:
        continue

    # if we have heard from enough beacons, verify that each beacon has reported
    # enough distance data
    keep_going = False
    for distances in beacon_distances.values():
        if len(distances) < BEACON_DIST_COUNT:
            keep_going = True
            break

    if keep_going is False:
        break

print("scan done. beacons accquired!")

print("computing average distances")
from statistics import mean
for beacon, distances in beacon_distances.items():
    beacons[beacon] = mean(distances)
print("done. beacon distances computed")

print("triangulating position using heard nodes")
# todo!
