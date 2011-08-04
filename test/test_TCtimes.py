#!/usr/bin/env python
# vim: sts=4 sw=4 et

import unittest, sys, tests_good, tests_bad, time, os
from ZSI import *
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

class TestCase(unittest.TestCase):
    '''Examples from "Definitive XML Schema, Priscilla Walmsley, p237-246
    '''
    def _check_data2data(self, tc, data, correct, msg):
        tmp = tc.text_to_data(data, None, None)
        stamp = tc.get_formatted_content(tmp)
        #print "%s -> %s" % (data, str(tmp))

        self.failUnless(stamp == correct, 
            '%s with local offset(%s): expecting "%s" got "%s"' %(
            msg, data, correct, stamp))

    def _wrap_timezone(self, f, *a, **kw):
        oldtz = os.environ.get('TZ', 'UTC')
        for tz in ['Europe/Moscow', 'Antarctica/Vostok', 'America/Los_Angeles', 'UTC']:
            try:
                os.environ['TZ'] = tz
                time.tzset()
                f(*a, **kw)
            finally:
                os.environ['TZ'] = oldtz
                time.tzset()

    def _check_minimum(self):
        data = "0001-01-01T00:00:00.0000000-07:00"
        tc = TC.gDateTime()
        tc.text_to_data(data, None, None)
    check_minimum = lambda s: s._wrap_timezone(s._check_minimum)

    def _check_datetime_timezone(self):
        # UTC with local timezone offset
        # Base example from http://www.w3.org/TR/xmlschema11-2/#dateTime-lexical-mapping

        correct = "2002-10-10T17:00:00Z"
        for t in ['2002-10-10T12:00:00-05:00', '2002-10-10T19:00:00+02:00', '2002-10-10T17:00:00+00:00', '2002-10-10T17:00:00Z']:
            self._check_data2data(TC.gDateTime(), t, correct, 'dateTime')
    check_datetime_timezone = lambda s: s._wrap_timezone(s._check_datetime_timezone)

    def _check_time_timezone(self):
        correct = "17:30:00Z"
        for t in ['12:30:00-05:00', '19:30:00+02:00', '17:30:00+00:00']:
            self._check_data2data(TC.gTime(), t, correct, 'time')
    check_time_timezone = lambda s: s._wrap_timezone(s._check_time_timezone)

    def _check_date_timezone(self):
        correct = "2002-10-10"
        for t in ['2002-10-10-05:00', '2002-10-10+02:00', '2002-10-10+00:00', '2002-10-10Z']:
            self._check_data2data(TC.gDate(), t, correct, 'date')
    check_date_timezone = lambda s: s._wrap_timezone(s._check_date_timezone)

    def check_valid_dateTime(self):
        typecode = TC.gDateTime()
        for i in ('1968-04-02T13:20:00', '1968-04-02T13:20:15.5', 
            '1968-04-02T13:20:00-05:00', '1968-04-02T13:20:00Z'):
            data = typecode.text_to_data(i, None, None)
            text = typecode.get_formatted_content(data)

    def check_parse_microseconds(self):
        good = (1968, 4, 2, 13, 20, 15, 511, 0, 0)
        typecode = TC.gDateTime()
        data = typecode.text_to_data('1968-04-02T13:20:15.511', None, None)
        self.failUnless(data == good,
            'did not parse something %s, not equal %s' %(data,good))

    def check_serialize_microseconds(self):
        dateTime = '1968-04-02T13:20:15.511Z'
        typecode = TC.gDateTime()
        text = typecode.get_formatted_content((1968, 4, 2, 13 - time.timezone / 3600, 20, 15, 511, 0, 0))
        self.failUnless(text == dateTime,
            'did not serialze correctly %s, not equal %s' %(text, dateTime))

    def check_serialize_microseconds_1000(self):
        bad = (1968, 4, 2, 13, 20, 15, 1000, 0)
        typecode = TC.gDateTime()
        self.failUnlessRaises(ValueError, typecode.get_formatted_content, bad)

    def check_serialize_microseconds_lessZero(self):
        '''ignore negative microseconds
        '''
        bad = (1968, 4, 2, 13, 20, 15, -1, 0)
        typecode = TC.gDateTime()
        text = typecode.get_formatted_content(bad)
        typecode.get_formatted_content(bad)

    def check_parse_microseconds2(self):
        good = (1968, 4, 2, 13 - time.timezone / 3600, 20, 15, 500, 0, 0)
        typecode = TC.gDateTime()
        data = typecode.text_to_data('1968-04-02T13:20:15.5Z', None,None)
        self.failUnless(data == good,
            'did not serialze correctly %s, not equal %s' %(data, good))

        #text = typecode.get_formatted_content((1968, 4, 2, 13, 20, 15, 5, 0, 500))
        #self.failUnless(text == dateTime,
        #    'did not serialze correctly %s, not equal %s' %(text, dateTime))

    def check_invalid_dateTime(self):
        typecode = TC.gDateTime()

    def check_valid_time(self):
        typecode = TC.gTime()
        for i in ('13:20:00', '13:20:30.5555', '13:20:00Z'):
            data = typecode.text_to_data(i, None, None)
            text = typecode.get_formatted_content(data)

    def broke_valid_time(self):
        typecode = TC.gTime()
        data = typecode.text_to_data('13:20:00-05:00', None, None)

    def check_invalid_time(self):
        typecode = TC.gTime()
        for i in ('5:20:00', '13:20.5:00',):
            self.failUnlessRaises(Exception, typecode.text_to_data, i, None, None),

    def broke_invalid_time_no_seconds(self):
        typecode = TC.gTime()
        i = '13:20:'
        self.failUnlessRaises(Exception, typecode.text_to_data, i, None, None)

    def broke_invalid_time_bad_timeofday(self):
        typecode = TC.gTime()
        i = '13:65:00'
        self.failUnlessRaises(Exception, typecode.text_to_data, i, None, None)

    def check_valid_date(self):
        typecode = TC.gDate()
        for i in ('1968-04-02', '-0045-01-01', '11968-04-02', '1968-04-02+05:00', '1968-04-02Z'):
            data = typecode.text_to_data(i, None, None)
            text = typecode.get_formatted_content(data)

    def check_invalid_date(self):
        typecode = TC.gDate()
        for i in ('68-04-02', '1968-4-2', '1968/04/02', '04-02-1968',):
            self.failUnlessRaises(Exception, typecode.text_to_data, i, None, None),

    def check_valid_cast(self):
        text = "2002-10-10T17:00:00Z"
        tc = TC.gDateTime()
        data = tc.text_to_data(text, None, None)

        tct = TC.gTime()
        tcd = TC.gDate()
        self.assertEquals("2002-10-10", tcd.get_formatted_content(data), "Invalid cast from gDateTime to gDate")
        self.assertEquals("17:00:00Z", tct.get_formatted_content(data), "Invalid cast from gDateTime to gTime")

    def broke_invalid_date_april31(self):
        # No checks for valid date April 30 days
        typecode = TC.gDate()
        self.failUnlessRaises(Exception, typecode.text_to_data, '1968-04-31', None, None),

    def check_gdates(self):
        def _assert_tc(tc, val, msg):
            self.assertEquals(val, tc.get_formatted_content(tc.text_to_data(val, None, None)), "%s: %s" % (msg, val))

        _assert_tc(TC.gYear(), '1984', "Invalid gYear")
        _assert_tc(TC.gYearMonth(), '1984-10', "Invalid gYearMonth")
        _assert_tc(TC.gMonth(), '--10', "Invalid gMonth")
        _assert_tc(TC.gMonthDay(), '--10-30', "Invalid gMonthDay")
        _assert_tc(TC.gDay(), '---30', "Invalid gDay")
        _assert_tc(TC.gDate(), '1984-10-30', "Invalid gDate")

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


