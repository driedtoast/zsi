#!/usr/bin/env python
############################################################################
# Joshua R. Boverhof, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import os, sys, unittest
from ServiceTest import main, ServiceTestCase, ServiceTestSuite
from ZSI import FaultException, ParsedSoap, SoapWriter
"""
Unittest 

WSDL:  wsdl/vim.wsdl
"""

# General targets
def dispatch():
    """Run all dispatch tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(VIMTestCase, 'test_dispatch'))
    return suite

def local():
    """Run all local tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(VIMTestCase, 'test_local'))
    return suite

def net():
    """Run all network tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(VIMTestCase, 'test_net'))
    return suite
    
def all():
    """Run all tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(VIMTestCase, 'test_'))
    return suite


class VIMTestCase(ServiceTestCase):
    name = "test_VIM25"
    client_file_name = "VimService_client.py"
    types_file_name  = "VimService_types.py"
    server_file_name = "VimService_server.py"

    def __init__(self, methodName):
        ServiceTestCase.__init__(self, methodName)
        self.wsdl2py_args.append('--lazy')
        self.wsdl2py_args.append('-b')

    def test_local_(self):
        # BUG 
        MSG = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope
xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body>
<RetrievePropertiesResponse xmlns="urn:vim25">
  <returnval>
    <obj type="VirtualMachine">vm-7220</obj>
    <propSet>
      <name>guest.disk</name>
      <val xsi:type="ArrayOfGuestDiskInfo">
        <GuestDiskInfo xsi:type="GuestDiskInfo">
          <diskPath>C:\</diskPath>
          <capacity>19312922624</capacity>
          <freeSpace>15236939776</freeSpace>
        </GuestDiskInfo>
      </val>
    </propSet>
  </returnval>
</RetrievePropertiesResponse>
</soapenv:Body>
</soapenv:Envelope>
"""

        # Parse it 
        ps = ParsedSoap(MSG)
        pyobj = ps.Parse( self.client_module.RetrievePropertiesResponseMsg.typecode )

if __name__ == "__main__" :
    main()

