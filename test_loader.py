'''
EXECUTE:
python -m pytest
'''

import os
import unittest

loader = unittest.TestLoader()
test_dir = '{0}/tests'.format(os.getcwd())
suite = loader.discover(test_dir)
print(suite)

runner = unittest.TextTestRunner()
runner.run(suite)

