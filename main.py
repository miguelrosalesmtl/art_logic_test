from art_logic import AParser
from art_logic.exceptions import AInvalidHexError, AMaximumValueError

while True:
   print('Choose an option:')
   print('1- Enter a string to decode')
   print('2- Show the decoded strings from part 2')
   print('3- exit')
   choice = input()
   choice.strip()

   if choice == '1':
      try:
         string = input()
         string.strip()
         parser = AParser(string)
         parser.convertSegment()
         parser.printInstructions()
      except AInvalidHexError as e:
         print(str(e))
   
   elif choice == '2':
      string = 'F0A04000417F4000417FC040004000804001C05F205F20804000'
      print("string: {0}".format(string))
      parser = AParser(string)
      parser.convertSegment()
      parser.printInstructions()

      string = 'F0A040004000417F417FC04000400090400047684F50573840008' +\
         '04001C05F204000400001400140400040007E405B2C4000804000'
      print("string: {0}".format(string))
      parser.setSegment(string)      
      parser.convertSegment()
      parser.printInstructions()

      string = 'F0A0417F41004000417FC0670867088' +\
         '04001C067082C3C18782C3C804000'
      print("string: {0}".format(string))
      parser.setSegment(string)
      parser.convertSegment()
      parser.printInstructions() 

   elif choice == '3':
      break
   else:
      print('***Invalid choice***\n')
