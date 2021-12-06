# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example scans for any BLE advertisements and prints one advertisement and one scan response
# from every device found. This scan is more detailed than the simple test because it includes
# specialty advertising types.

#Written by John Kothmann and G. Michael Fitzgerald
#Submitting tonight but we were unable to completely resolve the error, so we will be re-attempting tomorrow.
import math
from adafruit_ble import BLERadio
beacon_map = {
    'c2:00:7d:00:00:52':	[3.72, 6.71],
    'c2:00:7d:00:00:59':	[8.54, 3.54],
    'c2:00:7d:00:00:9f':	[7.79, 9.97],
    'c2:00:7d:00:03:92':	[15.58, 5.08],
    'c2:00:7d:00:03:8c':	[22.12, 5.08],
    'c2:00:7d:00:00:97':	[30.66, 7.11],
    'c2:00:7d:00:00:98':	[35.13, 5.08],
    'c2:00:7d:00:00:64':	[37.7, 6.62],
    'c2:00:7d:00:00:99':	[44.95, 5.08],
    'c2:00:7d:00:03:8e':	[52.45, 3.14],
    'c2:00:7d:00:00:9d':	[56.41, 7.64],
    'c2:00:7d:00:00:6d':	[52.18, 13.46],
    'c2:00:7d:00:03:6f':	[43.09, 13.46],
    'c2:00:7d:00:03:6e':	[49.89, 16.88],
    'c2:00:7d:00:00:68':	[52.11, 22.56],
    'c2:00:7d:00:00:69':	[57.51, 18.71],
    'c2:00:7d:00:00:6f':	[60.11, 23.49],
    'c2:00:7d:00:00:67':	[55.84, 30.42],
    'c2:00:7d:00:00:76':	[48.7, 28.83],
    'c2:00:7d:00:00:75':	[43.35, 22.65],
    'c2:00:7d:00:03:70':	[39.98, 24.37],
    'c2:00:7d:00:00:77':	[41.68, 28.86],
    'c2:00:7d:00:00:78':	[31.71, 26.85],
    'c2:00:7d:00:03:91':	[48.65, 20.65],
    'c2:00:7d:00:00:8f':	[31.45, 24.16],
    'c2:00:7d:00:00:62':	[22.13, 28.86],
    'c2:00:7d:00:03:8a':	[12.65, 22.63],
    'c2:00:7d:00:00:61':	[15.95, 13.48],
    'c2:00:7d:00:00:9c':	[13.59, 10.01],
    'c2:00:7d:00:00:8e':	[31.49, 18.98],
    'c2:00:7d:00:00:6b':	[37.8, 10.21],
    'c2:00:7d:00:00:8d':	[43.12, 18.71],
    'c2:00:7d:00:00:96':	[13.0, 26.87],
    'c2:00:7d:00:00:63':	[19.29, 1.97],
    'c2:00:7d:00:00:93':	[60.11, 13.09],
    'c2:00:7d:00:00:6e':	[54.36, 22.48],
    'c2:00:7d:00:03:6a':	[54.63, 18.88],
    'c2:00:7d:00:00:74':	[60.11, 20.25],
    'c2:00:7d:00:00:72':	[60.11, 26.8],
    'c2:00:7d:00:00:65':	[45.3, 22.48],
    'c2:00:7d:00:00:71':	[48.46, 19.33],
    'c2:00:7d:00:00:6a':	[33.79, 24.2],
    'c2:00:7d:00:00:5a':	[40.15, 18.81],
    'c2:00:7d:00:00:5c':	[19.89, 13.98],
    'c2:00:7d:00:00:9b':	[17.73, 14.54],
    'c2:00:7d:00:00:94':	[28.63, 28.86],
    'c2:00:7d:00:00:95':	[12.54, 23.69],
    'c2:00:7d:00:00:91':	[8.46, 30.39],
    'c2:00:7d:00:00:92':	[1.63, 30.4],
    'c2:00:7d:00:00:9e':	[1.5, 23.2],
    'c2:00:7d:00:00:60':	[1.46, 16.99],
    'c2:00:7d:00:00:9a':	[8.05, 16.06],
    'c2:00:7d:00:03:96':	[4.68, 16.88],
    'c2:00:7d:00:00:5f':	[5.2, 10.13],
}

from adafruit_ble.advertising import Advertisement, to_hex
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
found = set()
scan_responses = set()
beacon_distances = {}
beacons = {}
# variables to control how BLE packets are filtered
DATA_TYPE = 255 # "manufacturer specific"
MANUFACTURER = b'\x4c\x00' # Apple
APPLE_DATA_TYPE = 2 # iBeacon data
ATTENUATION = 0.1 # integer in [2, 6] to adjust for environmental circumstances
CALIBRATION = 1 # value to scale distance measurements

# variables to control how many beacons we need to hear from, and how much we
# need to hear from each beacon, before attempting position triangulation
BEACON_COUNT = 6
BEACON_DIST_COUNT = 3


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
        beacon_distances[MACAddress] = []
        print(MACAddress)
    
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
    print("Distances: ", beacon_distances[MACAddress])
    # keep listening for more beacon advertisements if we haven't heard from
    # enough beacons yet
    found_beacons = len(beacon_distances)
    print("foundbeacons: ", found_beacons)
    if found_beacons < BEACON_COUNT:
        continue
    # if we have heard from enough beacons, verify that each beacon has reported
    # enough distance data
    keep_going = True
    goodBeacons = 0
    for distances in beacon_distances.values():
        if len(distances) >= BEACON_DIST_COUNT:
            goodBeacons += 1
        if goodBeacons >= BEACON_COUNT:
            keep_going = False
    print("Goodbeacons: ", goodBeacons)
    if keep_going is False:
        break

print("scan done. beacons accquired!")

print("computing average distances")
for beacon, distances in beacon_distances.items():
    if len(distances) >= BEACON_DIST_COUNT:
        sumD = 0
        for d in distances:
            print("distance reading raw: ", d)
            sumD += d
        distancemean = sumD / len(distances)
        beacons[beacon] = distancemean
print("done. beacon distances computed")
print("We have ", len(beacons), " good beacons to use")

print("triangulating position using heard nodes")
usablebeacons = {}
for beacon, distance in beacons.items():
    if beacon in beacon_map:
        usablebeacons[beacon] = distance
print("We have ", len(usablebeacons), " usable beacons")
beacon1 = usablebeacons.popitem()
print("beacon 1 distance: ", beacon1[1])
beacon2 = usablebeacons.popitem()
print("beacon 2 distance: ", beacon2[1])
beacon1coords = beacon_map[beacon1[0]] #get first beacon coordinates
print("first coords: ", beacon1coords)
beacon2coords = beacon_map[beacon2[0]] #get second beacon coordinates
print("second coords: ", beacon2coords)
beacondist = math.sqrt(((beacon1coords[0] - beacon2coords[0]) ** 2) + ((beacon1coords[1] - beacon2coords[1]) ** 2))
print("Distance: ", beacondist)
x_coord = ((beacon1[1] ** 2) - (beacon2[1] ** 2) + beacondist ** 2) / (2 * beacondist)
y_coord = math.sqrt(abs((beacon1[1] ** 2) - (x_coord ** 2)))
print("Coordinates are X: ", (x_coord + beacon1coords[0]), " Y: ", + (y_coord + beacon1coords[1]))
