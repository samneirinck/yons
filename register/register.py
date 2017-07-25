import sys
import requests
import soco
from netifaces import interfaces, AF_INET, ifaddresses

data = [ifaddresses(i) for i in interfaces()]
inetInterfaces = ([d[AF_INET][0]['addr'] for d in data if d.get(AF_INET)])

inetInterface = None
for inetInterface in inetInterfaces:
    print('Looking for Sonos devices on network interface ' + inetInterface, end='... ')
    devices = soco.discover(interface_addr=inetInterface)
    if devices is None:
        print('None found')
        continue

    device = devices.pop()
    print("Found a Sonos device named '" + device.player_name + "'")
    break

if device is None:
    print('No Sonos installation found. Manual registration required')
    sys.exit(1)

musicServiceUri = 'http://' + inetInterface + ':8085/'
registrationUri = 'http://{}:1400/customsd'.format(device.ip_address)

params = {                                    
    'sid': 246,
    'name': 'YouTube',
    'uri': musicServiceUri,
    'secureUri': musicServiceUri,
    'pollInterval': 60,
    'authType': 'DeviceLink',
    'stringsVersion': 1,
    'stringsUri': musicServiceUri + '/static/strings.xml',
    'presentationMapVersion': 0,
    'presentationMapUri': '',
    'containerType': 'MService',
    'caps': 'search'
}

requests.post(registrationUri, data=params)