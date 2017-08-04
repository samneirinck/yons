"""Sonos MusicService implementation"""
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Fault, InternalError, Boolean, XmlAttribute

from spyne.protocol.soap import Soap11
from spyne.server.pyramid import PyramidApplication
from spyne.model.complex import ComplexModel

from lxml.builder import E

from spyne.server.pyramid import PyramidApplication
from pyramid.config import Configurator
from pyramid.view import view_config

import os

my_code = None

class SonosFriendlySoap(Soap11):
    def fault_to_parent(self, ctx, cls, inst, parent, ns, *args, **kwargs):
        subelts = [
            E("faultcode", inst.faultcode),
            E("faultstring", inst.faultstring),
            E("faultactor", inst.faultactor),
        ]

        x = self._fault_to_parent_impl(ctx, cls, inst, parent, ns, subelts)
        return x

class DeviceLinkCodeResult(ComplexModel):
    regUrl = Unicode
    linkCode = Unicode
    showLinkCode = bool
    linkDeviceId = Unicode

class AppLinkInfo(ComplexModel):
    appUrl = Unicode
    appUrlStringId = Unicode
    deviceLink = DeviceLinkCodeResult
    

class AppLinkResult(ComplexModel):
    authorizeAccount = AppLinkInfo

class DeviceAuthTokenResult(ComplexModel):
    authToken = Unicode
    privateKey = Unicode

class MediaCollection(ComplexModel):
    id = Unicode
    itemType = ItemType
    title = Unicode
    language = Unicode
    country = Unicode
    genreId = Unicode
    genre = Unicode
    twitterId = Unicode
    liveNow = Boolean
    onDemand = Boolean
    artist = Unicode
    artistId = Unicode
    canScroll = Boolean
    canPlay = Boolean
    canEnumerate = Boolean
    canAddToFavorites = Boolean
    canCache = Boolean
    canSkip = Boolean
    albumArtURI = Unicode
    authRequired = Boolean
    homogeneous = Boolean
    canAddToFavorite = Boolean
    readOnly = XmlAttribute(Boolean)
    userContent = XmlAttribute(Boolean)
    renameable = XmlAttribute(Boolean)
    containsFavorite = Boolean

class MediaList(ComplexModel):
    index = Integer
    count = Integer
    total = Integer
    mediaCollection = MediaCollection
    mediaMetadata = MediaMetadata




class MusicService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def getDeviceLinkCode(ctx, houseHoldId):
        # Ideally, return a fault here, but this seems to do the trick as well
        raise Fault('Client.AuthTokenExpired', 'Client.AuthTokenExpired')

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=AppLinkResult)
    def getAppLink(ctx, householdId, hardware, osVersion, sonosAppName, callbackPath):
        result = AppLinkResult()

        result.authorizeAccount = AppLinkInfo()
        result.authorizeAccount.appUrlStringId = 'SIGN_IN'
        
        result.authorizeAccount.deviceLink = DeviceLinkCodeResult()
        result.authorizeAccount.deviceLink.regUrl = 'https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&response_type=code&state=' + householdId + '&redirect_uri=http://localhost:8085/auth/&client_id=364976931191-i133fs9o6c0d1giddr49flckk7mpk77h.apps.googleusercontent.com'
        result.authorizeAccount.deviceLink.linkCode = householdId
        result.authorizeAccount.deviceLink.showLinkCode = False

        return result

    @rpc(Unicode, Unicode, Unicode, _returns=DeviceAuthTokenResult)
    def getDeviceAuthToken(ctx, householdId, linkCode, linkDeviceId):
        global my_code
        if my_code is not None:
            result = DeviceAuthTokenResult()

            result.authToken = my_code
            result.privateKey = 'KEY' 
            return result
        else:
            raise Fault('Client.NOT_LINKED_RETRY', 'Access token not found, retry', detail={'SonosError': 5})
 

    @rpc(Integer, Unicode, Integer, Boolean)
    def getMetadata(ctx, count, id, index, recursive):
        return "hello"


soapApp = view_config(route_name="home")(
    PyramidApplication(Application([MusicService], 'http://www.sonos.com/Services/1.1',
                          in_protocol=SonosFriendlySoap(),
                          out_protocol=SonosFriendlySoap())))


@view_config(route_name='auth')
def my_view(request):
    from pyramid.response import Response

    global my_code
    my_code = request.GET['code']

    return Response('Return to SONOS app')

if __name__ == '__main__':
    settings = {'debug_all': True}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    

    config = Configurator(settings=settings)
    config.add_static_view('static', path=path)
    config.add_route('home', '/')
    config.add_route('auth', '/auth/')
    config.scan()
    wsgi_app = config.make_wsgi_app()
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8085, wsgi_app)
    server.serve_forever()
