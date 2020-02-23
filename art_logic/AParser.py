from .AEncoder import AEncoder


class AParser:
   ''' Parser class '''
   CLR = 'F0'
   PEN = '80'
   CO = 'A0'
   MV = 'C0'

   COMMANDS = [CLR, PEN, CO, MV]

   PEN_UP = 'UP'
   PEN_DOWN = 'DOWN'

   def __init__(self, segment):
      self.__penStatus = AParser.PEN_UP
      self.__currentCoordinates = (0, 0)
      self.__encoder = AEncoder()
      self.__segment = segment
      self.__instructions = []
      self.__segmentArray = \
         [(self.__segment[i:i+2]) for\
            i in range(0, len(self.__segment), 2)]

   def setSegment(self, segment):
      self.__penStatus = AParser.PEN_UP
      self.__currentCoordinates = (0, 0)
      self.__segment = segment
      self.__instructions = []
      self.__segmentArray = \
         [(self.__segment[i:i+2]) for\
            i in range(0, len(self.__segment), 2)]

   def convertSegment(self):
      ''' Converts the segments in commands '''
      idx = 0
      while idx < len(self.__segmentArray):
         # CLEAR
         if self.__segmentArray[idx] == AParser.CLR:
               idx = self.processCLRInstruction(idx)
         # PEN
         elif self.__segmentArray[idx] == AParser.PEN:
               idx = self.processPENInstruction(idx)
         # COLOR
         elif self.__segmentArray[idx] == AParser.CO:
               idx = self.processCOInstruction(idx)
         # MOVEMENT
         elif self.__segmentArray[idx] == AParser.MV:
               idx = self.processMVInstruction(idx)
         else:
               # skip if byte-instruction not recognized
               idx += 1

   def processCLRInstruction(self, idx):
      self.__instructions.append('CLR;\n')
      idx += 1
      return idx

   def processPENInstruction(self, idx):
      if idx+2 < len(self.__segmentArray):
         convertedValue = self.__encoder.decode(
               *self.__segmentArray[idx+1:idx+3])
         self.__penStatus = AParser.PEN_UP \
               if convertedValue == 0 else AParser.PEN_DOWN
         self.__instructions.append(
               'PEN {0};\n'.format(self.__penStatus))
         idx += 3
      else:
         idx += 1
      return idx

   def processCOInstruction(self, idx):
      if idx+9 < len(self.__segmentArray):
         decodedArgs = self.decodeColorArgs(self.__segmentArray[idx+1:idx+9])
         if decodedArgs is not None:
               self.__instructions.append(
                  str("CO {0} {1} {2} {3};\n".format(*decodedArgs)))
               idx += 9
         else:
               idx += 1
      else:
         idx += 1
      return idx

   def processMVInstruction(self, idx):
      args = []
      intersects = []
      idx += 1
      absoluteCoord = self.__currentCoordinates
      while idx + 3 < len(self.__segmentArray):

         # If byte has a leading 1 quit parsing MV arguments
         if int(self.__segmentArray[idx], 16) > int('7F', 16):
               break

         isXValid = self.validateBytePairs(
               self.__segmentArray[idx: idx+2])
         isYValid = self.validateBytePairs(
               self.__segmentArray[idx+2: idx+4])
         
         if isXValid and isYValid:
               displacementVector = self.decodeMovementArgs(
                  self.__segmentArray[idx: idx+4])
               originCoord = absoluteCoord
               absoluteCoord = (
                  absoluteCoord[0] + displacementVector[0],
                  absoluteCoord[1] + displacementVector[1])
               intersects.append(self.getBoundariesIntersects(originCoord,
                  absoluteCoord))
               args.append(absoluteCoord)
               idx += 4
      # Once the sequence of dots representing
      # the cursor displacement is collected
      # it can be translated to a set of instructions
      if args != [] and self.__penStatus == AParser.PEN_DOWN:
         instructions, self.__currentCoordinates = self.getMVInstructions(args,
               intersects,
               self.__currentCoordinates)
         if len(instructions) > 0:
               self.__instructions.extend(instructions)

      elif args != [] and self.__penStatus == AParser.PEN_UP:
         self.__currentCoordinates = args.pop()
         self.__instructions.append("MV {0};\n".format(self.__currentCoordinates))
      return idx

   def getMVInstructions(
      self,
      pointsArray,
      cursorIntersectsArray,
      realPosition):
      ''' returns a decoded MV instruction list '''

      pointsArray.insert(0, realPosition)
      idx = 0
      instructions = []        
      accumulator = []

      while idx < len(cursorIntersectsArray):

         # vector does not cross boundaries
         if len(cursorIntersectsArray[idx]) == 0:

               # vector is inside boundaries
               if self.isPtInsideBoundaries(pointsArray[idx]):
                  accumulator.append(pointsArray[idx+1])

               realPosition = pointsArray[idx+1]

         # vector crossed boundary once
         elif len(cursorIntersectsArray[idx]) == 1:
               intersectCoordinates = cursorIntersectsArray[idx]

               # vector direction exiting boundaries
               if self.isPtInsideBoundaries(pointsArray[idx]):
                  accumulator.append(cursorIntersectsArray[idx][0])
                  instructions.append("MV {0};\n"\
                           .format(('{} '*len(accumulator))\
                           .format(*accumulator).rstrip()))
                  instructions.append("PEN UP;\n")
                  accumulator = []
                  realPosition = pointsArray[idx+1]

               # vector direction entering boundaries
               else:
                  accumulator.append(pointsArray[idx+1])
                  instructions.append("MV {0};\n".format(
                     cursorIntersectsArray[idx][0]))
                  instructions.append("PEN DOWN;\n")
                  instructions.append("MV {0};\n"\
                     .format(('{} '*len(accumulator))\
                     .format(*accumulator).rstrip()))
                  accumulator = []
                  realPosition = pointsArray[idx+1]

         # line crossed boundary twice
         elif len(cursorIntersectsArray[idx]) == 2:
               instructions.append("MV {0} {1};\n".format(
                  cursorIntersectsArray[idx][0],
                  cursorIntersectsArray[idx][1]))
               instructions.append("PEN UP;\n")
               accumulator = []
               realPosition = pointsArray[idx+1]             
         idx += 1

      if 0 < len(accumulator):
         instructions.append("MV {0};\n".format(('{} '*len(accumulator))\
            .format(*accumulator).rstrip()))
      return instructions, realPosition

   def isPtInsideBoundaries(self, pt):
      ''' verifies a point in inside the boundaries '''
      return True if -8192 <= pt[0] and pt[0] <= 8191 and\
               -8192 <= pt[1] and pt[1] <= 8191 else False

   def decodeColorArgs(self, byteArray):
      ''' 
      Decode color Arguments
      returns An array containing the decoded values [x1, x2, x3, x4]
      or None
      '''
      if self.validateBytePairs(byteArray, 8) is False:
         return None

      return [
         self.__encoder.decode(*byteArray[0:2]),
         self.__encoder.decode(*byteArray[2:4]),
         self.__encoder.decode(*byteArray[4:6]),
         self.__encoder.decode(*byteArray[6:])]

   def decodeMovementArgs(self, byteArray):
      ''' Returns a tuplet from an array of 2 bytes '''

      arg1 = self.__encoder.decode(*byteArray[0:2])
      arg2 = self.__encoder.decode(*byteArray[2:4])
      return (arg1, arg2)

   def validateBytePairs(self, bytePairs, expectedBytes=None):
      ''' Validates if a pair of bytes consists of allowed chars '''
      if expectedBytes is None:
         if len(bytePairs) % 2 and len(bytePairs) != 0:
               return False
      else:
         if len(bytePairs) != expectedBytes:
               return False
      i = 0
      while i + 1 < len(bytePairs):
         if self.__encoder.validateBytePair(bytePairs[i],
           bytePairs[i+1]) is False:
            return False
         i += 2
      return True

   def getIntersectsArray(self, pointsArray):
      ''' returns a list of intersections '''
      intersectsArray = []
      idx = 0
      while idx < len(pointsArray)-1:
         intersectsArray.append(self.getBoundariesIntersects(pointsArray[idx],
            pointsArray[idx+1]))
         idx += 1
      return intersectsArray
      
   def getIntersection(self, p0, p1, p2, p3) :
      '''
      from 
      https://stackoverflow.com/questions/563198/
      how-do-you-detect-where-two-line-segments-intersect
      '''
      s10_x = p1[0] - p0[0]
      s10_y = p1[1] - p0[1]
      s32_x = p3[0] - p2[0]
      s32_y = p3[1] - p2[1]

      denom = s10_x * s32_y - s32_x * s10_y

      if denom == 0 :
         return None # parallel

      denom_is_positive = denom > 0
      s02_x = p0[0] - p2[0]
      s02_y = p0[1] - p2[1]

      s_numer = s10_x * s02_y - s10_y * s02_x
      if (s_numer < 0) == denom_is_positive :
         return None # no intersection

      t_numer = s32_x * s02_y - s32_y * s02_x
      if (t_numer < 0) == denom_is_positive :
         return None # no intersection

      if (s_numer > denom) == denom_is_positive or\
        (t_numer > denom) == denom_is_positive:
         return None # no intersection     

      t = t_numer / denom

      x = p0[0] + (t * s10_x)
      y = p0[1] + (t * s10_y)

      if x > 0:
         xBias = 0.000000001
      else:
         xBias = -0.000000001
      if y > 0:
         yBias = 0.000000001
      else:
         yBias = -0.000000001
      intersection_point = (
         round(x + xBias),
         round(y + yBias))
      return intersection_point

   def getBoundariesIntersects(self, p1, p2):
      '''
      calculates the intersections of a vector and
      the boundaries of canvas.
      '''
      intersects = []

      # - x
      left_limit = [(-8192, -8192), (-8192, 8191)]
      pt = self.getIntersection(p1, p2, *left_limit)
      if pt is not None:
         intersects.append(pt)

      # + x
      right_limit = [(8191, -8192), (8191, 8191)]
      pt = self.getIntersection(p1, p2, *right_limit)
      if pt is not None:
         intersects.append(pt)

      # - y
      bottom_limit = [(-8192, -8192), (8191, -8192)]
      pt = self.getIntersection(p1, p2, *bottom_limit)
      if pt is not None:
         intersects.append(pt)

      # + y
      upper_limit = [(-8192, 8191), (8191, 8191)]
      pt = self.getIntersection(p1, p2, *upper_limit)
      if pt is not None:
         intersects.append(pt)

      return intersects

   def getInstructions(self):
      return self.__instructions

   def instructionsToString(self):
      return ''.join(self.__instructions)

   def printInstructions(self):
      print(self.instructionsToString())
