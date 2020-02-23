import unittest
from .context import AEncoder, AInvalidHexError, AMaximumValueError

import unittest
import pytest

class ATestAEncoder(unittest.TestCase):
    ''' decoding test '''

    def setUp(self):
        ''' setUp fixtures '''
        self.encoder = AEncoder()
    
    def testGoodEncode(self):
        ''' good encoding tests '''
        inputs = [0, -8192, 8191, 2048, -4096]
        outputs = ['0x4000', '0x0000', '0x7F7F', '0x5000', '0x2000']
        counter = 0
        for inp in inputs:
            self.assertEqual(
                self.encoder.encode(inp),
                outputs[counter])
            counter += 1
    
    def testBadEncode(self):
        ''' bad encoding tests '''
        inputs = [-48964, 456946]

        with pytest.raises(AMaximumValueError):
            assert self.encoder.encode(inputs[0])
            assert self.encoder.encode(inputs[1])
    
    def testGoodDecode(self):
        ''' Good decoding test '''
        inputs = [
            ('40' , '00'),
            ('00', '00'),
            ('7F', '7F'),
            ('50', '00'),
            ('0A', '05'),
            ('55', '00')]
        outputs = [0, -8192, 8191, 2048, -6907, 2688]
        counter = 0
        for i in inputs:
            self.assertEqual(self.encoder.decode(*i), outputs[counter])
            counter += 1

    def testBadDecode(self):
        ''' Bad decoding test '''
        inputs = [
            ('NM', 'OK'),
            ('XX', 'RR')]
        with pytest.raises(AInvalidHexError):
            self.encoder.decode(*inputs[0])
            self.encoder.decode(*inputs[1])
