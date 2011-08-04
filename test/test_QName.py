#!/usr/bin/env python
import unittest, sys, tests_good, tests_bad, time
from ZSI import *
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


"""Bug [ 1520092 ] URI Bug: urllib.quote escaping reserved chars
   Bug [ 2748314 ] Malformed type attribute (bad NS) with 2.1a1 but not with 2.
"""


class TestCase(unittest.TestCase):
    def check_soapfault_faultcode(self):
        """ Typecode QName when default namespace is not declared, should
        specify the empty namespace.
        """ 
        msg = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body>
<soapenv:Fault>
   <faultcode>ServerFaultCode</faultcode>
   <faultstring>Operation failed since VMware tools are not running in this virtual machine.</faultstring>
   <detail>
     <ToolsUnavailableFault xmlns="urn:vim2"/>
   </detail>
</soapenv:Fault>
</soapenv:Body>
</soapenv:Envelope>"""

        from ZSI import ParsedSoap, FaultFromFaultMessage
        ps = ParsedSoap(msg)
        fault = FaultFromFaultMessage(ps)
        self.failUnless(fault.code == ('','ServerFaultCode'), 'faultcode should be (namespace,name) tuple')

    def check_type_attribute_qname_in_default_ns(self):
        msg = """
<ns1:test xsi:type="int" xmlns:ns1="urn:vim25" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns="http://www.w3.org/2001/XMLSchema">
100
</ns1:test>"""
        ps = ParsedSoap(msg, envelope=False)
        pyobj = ps.Parse(TC.Integer(pname=("urn:vim25","test")))



#
# Creates permutation of test options: "check", "check_any", etc
#
_SEP = '_'
for t in [i[0].split(_SEP) for i in filter(lambda i: callable(i[1]), TestCase.__dict__.items())]:
    test = ''
    for f in t:
        test += f
        if globals().has_key(test): test += _SEP; continue
        def _closure():
            name = test
            def _makeTestSuite():
                suite = unittest.TestSuite()
                suite.addTest(unittest.makeSuite(TestCase, name))
                return suite
            return _makeTestSuite

        globals()[test] = _closure()
        test += _SEP


makeTestSuite = check
def main():
    unittest.main(defaultTest="makeTestSuite")
if __name__ == "__main__" : main()

