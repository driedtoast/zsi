#!/usr/bin/env python
############################################################################
# Joshua R. Boverhof, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import sys
from ZSI import ServiceContainer, Fault
from ZSI.ServiceContainer import AsServer, ServiceSOAPBinding
from NoMessagePartServer_server import NoMessagePartServer

class Service(NoMessagePartServer):
    def soap_Hello(self, ps, **kw):
        request,response = NoMessagePartServer.soap_Hello(self, ps, **kw)

        if request is not None:
            raise RuntimeException, "REQUEST SHOULD BE NONE"
        response.Result = "XXX"
        return request,response


def twisted_main(port):
    from twisted.internet import reactor
    from twisted.application import service, internet
    from twisted.web.resource import Resource
    from twisted.web.server import Site

    root = Resource()
    root.putChild('test', Service())
    reactor.listenTCP(port, Site(root))

def main():
    port = int(sys.argv[1])
    if issubclass(NoMessagePartServer, ServiceSOAPBinding):
        AsServer(port, (Service('test'),))
        return

    #from ZSI.twisted.WSresource import WSResource
    #if issubclass(NoMessagePartServer, WSResource):
    from twisted.internet import reactor
    reactor.callWhenRunning(twisted_main, port)
    reactor.run()


if __name__ == "__main__" :
    main()
