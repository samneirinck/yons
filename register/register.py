import urllib
import socket
import sys
import requests
import soco
import logging

logging.basicConfig(level=logging.DEBUG)

print('Looking for Sonos installation')


device = soco.discovery.discover(interface_addr='192.168.0.179')
if device is None:
    print('No Sonos installation found. Manual registration required')
    sys.exit(1)

print('Sonos installation found. Registering music service on ' + device.ip_address)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",53))

registrationUri =  'http://{}:1400/customsd.htm'.format(device.ip_address)
print(registrationUri)
uri = 'http://{}:8085/'.format(s.getsockname()[0])
s.close()

params = {
    'sid': 246,
    'name': 'YouTube',
    'uri': uri,
    'secureUri': uri,
    'pollInterval': 60,
    'authType': 'DeviceLink',
    'stringsVersion': 1,
    'stringsUri': uri + '/static/strings.xml',
    'presentationMapVersion': 0,
    'presentationMapUri': '',
    'containerType': 'MService',
    'caps': 'search'
}

#r = requests.post()
