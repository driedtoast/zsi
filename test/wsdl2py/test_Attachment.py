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

WSDL:   
"""

# General targets
def dispatch():
    """Run all dispatch tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(TestCase, 'test_dispatch'))
    return suite

def local():
    """Run all local tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(TestCase, 'test_local'))
    return suite

def net():
    """Run all network tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(TestCase, 'test_net'))
    return suite
    
def all():
    """Run all tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(TestCase, 'test_'))
    return suite


class TestCase(ServiceTestCase):
    name = "test_Attachment"
    client_file_name = "TestService_client.py"
    types_file_name  = "TestService_types.py"
    server_file_name = "TestService_server.py"

    def __init__(self, methodName):
        ServiceTestCase.__init__(self, methodName)
        self.wsdl2py_args.append('-b')

    def test_local_generateMessageAttachment(self):
        """doc/lit, generating a message using MIME attachment, 
        we don't have the server side implementation so we can 
        really do a full test yet
        """
        from TestService_server import uploadFileRequest
        #stubs were properly generated
        request = uploadFileRequest()
        request._name = "TestService_client.py"
        request._attachment = open("stubs/TestService_client.py", 'r')
        sw = SoapWriter({}, header=True, outputclass=None, encodingStyle=None)
        sw.serialize(request)
        print "the request message is: " + str(sw)
        #there is not server side, so for the moment we just create the message and print it on screen
        #TODO add server side implmementation


if __name__ == "__main__" :
    main()
