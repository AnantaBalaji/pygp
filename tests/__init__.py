import unittest

from pygp.parser import Parser, _generator
from pygp.graph import construct_graph, Graph
import logging
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

class TestPYGP(unittest.TestCase):
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

    def test_graph(self):
        uniques = [1, 2, 3, 4]
        as_paths = [[2, 3, 1], [4, 1, 3], [3, 4, 2]]
        G = construct_graph(uniques, as_paths)
        v = G.getVertex(1)
        self.assertIsNotNone(v)

    def test_parser_construct_graph(self):
        p = Parser(dataset="../dataset/destfile")
        grp = p.graph
        self.assertIsNotNone(grp)