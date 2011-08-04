#!/usr/bin/env python
############################################################################
# Joshua R. Boverhof, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import os, sys, unittest
from ServiceTest import main, ServiceTestCase, ServiceTestSuite
from ZSI import FaultException, SoapWriter, ParsedSoap
"""
Unittest 

[ 1803439 ] ZSI.generate.Wsdl2PythonError: must specify part for doc/lit

Date: 2008-10-15 18:42
Sender: boverhof
Here is the offending entity:

	<wsdl:message name="HelloRequest"/>

From
http://www.ws-i.org/Profiles/BasicProfile-1.0-2004-04-16.html#WSDLMSGS

      Use of wsdl:message elements with zero parts is permitted in
Document styles to permit operations that can send or receive messages with
empty soap:Bodys.

Basically what needs to be done here is an empty <soap:Body> is sent...  

Now only ONE operation should be able to specify an message w/o a part (
for doc/lit ), because the wire representation of each operation MUST be
unique.

WSDL:   wsdl/NoMessagePart.wsdl
"""

# General targets
def dispatch():
    """Run all dispatch tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(NoMessagePartTestCase, 'test_dispatch'))
    return suite

def local():
    """Run all local tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(NoMessagePartTestCase, 'test_local'))
    return suite

def net():
    """Run all network tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(NoMessagePartTestCase, 'test_net'))
    return suite
    
def all():
    """Run all tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(NoMessagePartTestCase, 'test_'))
    return suite


class NoMessagePartTestCase(ServiceTestCase):
    name = "test_NoMessagePart"
    client_file_name = "NoMessagePartServer_client.py"
    types_file_name  = "NoMessagePartServer_types.py"
    server_file_name = "NoMessagePartServer_server.py"

    def __init__(self, methodName):
        ServiceTestCase.__init__(self, methodName)
        self.wsdl2py_args.append('-b')

    def test_local_NoMessagePart(self):
        ## msg = self.client_module.HelloRequest()
        msg = None
        rsp = self.client_module.HelloResponse()

        # Core functionality required
        s = SoapWriter()
        xml = str(s)

        print xml

        # Core functionality required
        ps = ParsedSoap(xml)

        self.failUnless(ps.body.childNodes == 0, "Empty Body expected: " + ps.body.childNodes)
        self.failUnless(ps.body_root == None, "Body root should be None: " + ps.body_root)

        pyobj = ps.Parse(None)

        self.failUnless(pyobj == None, "pyobj should be None: " + pyobj)


    def test_dispatch_NoMessagePart(self):
        loc = self.client_module.NoMessagePartServerLocator()
        port = loc.getHelloServerSOAP11port_http(**self.getPortKWArgs())
        
        ## NOTE: Should take no argument
        rsp = port.Hello()
        self.failUnless(rsp.Return == "XXX", "TODO")


if __name__ == "__main__" :
    main()

