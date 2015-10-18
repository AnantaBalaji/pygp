import unittest

from pygp.parser import Parser, _generator
import logging
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

class TestParser(unittest.TestCase):
    """
       Used to Test the parser which generates the parsed
       data from the results.
    """
    def test_map_filter(self):
        """
          Map filter from the Parse class
        """
        p = Parser(dataset="../dataset/testset")
        self.assertIsNotNone(p.actual_values)

    def test_generates(self):
        a = [[1, 2], [3]]
        self.assertListEqual(list(_generator(a)), [1, 2, 3])
