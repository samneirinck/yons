"""Registers the MusicService to the Sonos system"""
import sys
import requests
import soco
from netifaces import interfaces, AF_INET, ifaddresses

DATA = [ifaddresses(i) for i in interfaces()]
INET_INTERFACES = ([d[AF_INET][0]['addr'] for d in DATA if d.get(AF_INET)])

INET_INTERFACE = None
for INET_INTERFACE in INET_INTERFACES:
    print('Looking for Sonos devices on network interface ' + INET_INTERFACE, end='... ')
    devices = soco.discover(interface_addr=INET_INTERFACE)
    if devices is None:
        print('None found')
        continue

    device = devices.pop()
    print("Found a Sonos device named '" + device.player_name + "'")
    break

if device is None:
    print('No Sonos installation found. Manual registration required')
    sys.exit(1)

MUSIC_SERVICE_URI = 'http://' + INET_INTERFACE + ':8085/'
REGISTRATION_URI = 'http://{}:1400/customsd'.format(device.ip_address)

PARAMS = {
    'sid': 246,
    'name': 'YouTube',
    'uri': MUSIC_SERVICE_URI,
    'secureUri': MUSIC_SERVICE_URI,
    'pollInterval': 60,
    'authType': 'DeviceLink',
    'stringsVersion': 1,
    'stringsUri': MUSIC_SERVICE_URI + '/static/strings.xml',
    'presentationMapVersion': 0,
    'presentationMapUri': '',
    'containerType': 'MService',
    'caps': 'search'
}

requests.post(REGISTRATION_URI, data=PARAMS)
