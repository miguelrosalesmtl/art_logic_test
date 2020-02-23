import pytest
import unittest
from .context import AParser

class ATestAParser(unittest.TestCase):

   def setUp(self):
      self.parser = AParser('')
   
   def testgetBoundriesIntersects(self):
      # - X
      test_val = [(0,0), (-10000, 0)]
      intersect = self.parser.getBoundariesIntersects(test_val[0], test_val[1])
      self.assertEqual(intersect, [(-8192, 0)])
      # + X
      test_val = [(0,0), (10000, 0)]
      intersect = self.parser.getBoundariesIntersects(test_val[0], test_val[1])
      self.assertEqual(intersect, [(8191, 0)])

      # - Y
      test_val = [(0,0), (0, -10000)]
      intersect = self.parser.getBoundariesIntersects(test_val[0], test_val[1])
      self.assertEqual(intersect, [(0, -8192)])

      # + Y
      test_val = [(0,0), (0, 10000)]
      intersect = self.parser.getBoundariesIntersects(test_val[0], test_val[1])
      self.assertEqual(intersect, [(0, 8191)])

   def testCornerIntersect(self):
      test_val = [(0,0), (10000, 10000)]
      intersect = self.parser.getBoundariesIntersects(test_val[0], test_val[1])
      self.assertEqual(intersect, [(8191, 8191)])

   def testInvalidString(self):
      self.parser.setSegment('FAILTHIS')
      self.parser.convertSegment()
      self.assertEqual(self.parser.getInstructions(), [])

   def testGreenLine(self):
      string = 'F0A04000417F4000417FC040004000804001C05F205F20804000'
      control = 'CLR;\nCO 0 255 0 255;\nMV (0, 0);\n' +\
         'PEN DOWN;\nMV (4000, 4000);\nPEN UP;\n'
      self.parser.setSegment(string)
      self.parser.convertSegment()
      self.assertEqual(self.parser.instructionsToString(), control)
   
   def testBlueSquare(self):
      string = 'F0A040004000417F417FC04000400090400047684F5057384000804'+\
         '001C05F204000400001400140400040007E405B2C4000804000'
      control = 'CLR;\nCO 0 0 255 255;\nMV (0, 0);\nPEN DOWN;\n' +\
         'MV (4000, 0) (4000, -8000) (-4000, -8000) (-4000, 0) (-500, 0);\n' +\
         'PEN UP;\n'
      self.parser.setSegment(string)
      self.parser.convertSegment()
      self.assertEqual(self.parser.instructionsToString(), control)

   
   def testEdge1(self):
      string = 'F0A0417F40004000417FC067086708804001C0670840004000187818784000804000'
      control = 'CLR;\nCO 255 0 0 255;\nMV (5000, 5000);\nPEN DOWN;\n' +\
         'MV (8191, 5000);\nPEN UP;\nMV (8191, 0);\nPEN DOWN;\n' +\
         'MV (5000, 0);\nPEN UP;\n'
      self.parser.setSegment(string)
      self.parser.convertSegment()
      self.assertEqual(self.parser.instructionsToString(), control)


   def testEdge2(self):
      string = 'F0A0417F41004000417FC067086708804001C067082C3C18782C3C804000'
      control = 'CLR;\nCO 255 128 0 255;\nMV (5000, 5000);\nPEN DOWN;\n' +\
         'MV (8191, 3405);\nPEN UP;\nMV (8191, 1596);\nPEN DOWN;\n'+\
         'MV (5000, 0);\nPEN UP;\n'
      self.parser.setSegment(string)
      self.parser.convertSegment()
      self.assertEqual(self.parser.instructionsToString(), control)
   