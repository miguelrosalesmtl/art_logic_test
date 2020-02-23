import re
from .exceptions import AMaximumValueError, AInvalidHexError

class AEncoder:

   def validateDecimalNumber(self, number):
      ''' number validation method '''
      if number < -8192 or 8191 < number:
         return False
      else:
         return True

   def validateBytePair(self, bytePair1, bytePair2):
      ''' byte pair validation, e.g. FF & FF '''
      if len(re.findall('^[0-9a-fA-F]{4}$', bytePair1 + bytePair2)) != 1:
         return False
      else:
         return True

   def encode(self, number):
      ''' encoding method '''
      if not self.validateDecimalNumber(number):
         raise AMaximumValueError(number, "Number not in range [-8192, 8191].")
      self.validateDecimalNumber(number)
      number += 8192
      low = number & 0x7f
      high = (number & 0x3f80)<<1
      return "0x{:04X}".format(high + low, 6)

   def decode(self, bytePair1, bytePair2):
      ''' decoding method '''
      if not self.validateBytePair(bytePair1, bytePair2):
         raise AInvalidHexError(bytePair1 + bytePair2,
            "Invalid Byte pair in string")
      encoded = int(bytePair1 + bytePair2, 16)
      low = encoded & 0x7f
      high = (encoded>>1)&0x3f80
      return (high + low) - 8192
