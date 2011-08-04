#!/usr/bin/env python
############################################################################
# Joshua R. Boverhof, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import os, sys, unittest
from ServiceTest import main, ServiceTestCase, ServiceTestSuite
from ZSI import FaultException
from ZSI.TC import _get_global_element_declaration as GED
from ZSI.writer import SoapWriter

from xml.etree import ElementTree

"""
Unittest for Bug Report 
[ 1853368 ] "elementFormDefault='unqualified'" mishandled

WSDL:  
"""

# General targets
def dispatch():
    """Run all dispatch tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(UnqualifiedTestCase, 'test_dispatch'))
    return suite

def local():
    """Run all local tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(UnqualifiedTestCase, 'test_local'))
    return suite

def net():
    """Run all network tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(UnqualifiedTestCase, 'test_net'))
    return suite
    
def all():
    """Run all tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(UnqualifiedTestCase, 'test_'))
    return suite


class UnqualifiedTestCase(ServiceTestCase):
    name = "test_Unqualified"
    types_file_name = "test_Unqualified_xsd_types.py"
 
    def __init__(self, methodName):
        ServiceTestCase.__init__(self, methodName)
        self.wsdl2py_args.append('-b')
        self.wsdl2py_args.append('-x')
 
    def test_local_serialize1(self):
        _test_local_serialize1()
 
def _test_local_serialize1():
        """
      <element name="GlobalElementLocalType">
          <complexType>
            <sequence>
              <element name="Unqualified1">
                  <complexType/>
              </element>
              <element name="Unqualified2" type="xsd:int"/>
              <element name="Unqualified3" type="tns:GlobalType"/>

              <element name="Unqualified4">
                  <simpleType>
                       <restriction base="xsd:string"/>
                  </simpleType>
              </element>

            </sequence>
          </complexType>
      </element>
        """
        tns = "urn:test"
        pyobj = GED(tns, "GlobalElementLocalType").pyclass()
        pyobj.Unqualified1 = pyobj.new_Unqualified1()
        pyobj.Unqualified2 = 2

        pyobj.Unqualified3 = pyobj.new_Unqualified3()
        pyobj.Unqualified3.Unqualified1 = pyobj.Unqualified3.new_Unqualified1()
        pyobj.Unqualified3.Unqualified2 = 32

        pyobj.Unqualified4 = "whatever"

        sw = SoapWriter(envelope=False)
        sw.serialize(pyobj)
        xml = str(sw)
        print xml

        et = ElementTree.fromstring(xml)
 
        # GlobalElementLocalType
        assert(et.tag == '{urn:test}GlobalElementLocalType'), "root GED"

        for i,j in zip([ 'Unqualified1', 'Unqualified2', 'Unqualified3', 'Unqualified4'], 
            map(lambda c: c.tag, et.getchildren())):

            assert(i == j), 'Match Failed: expected "%s" not "%s"' %(i,j)
        
        

if __name__ == "__main__" :
    main()

