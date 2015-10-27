import unittest

from pygp.parser import Parser, _generator
from pygp.graph import construct_graph, Graph
from pygp.Analysis import Analyser

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
        log.info(p.as_paths)
        self.assertIsNotNone(p.actual_values)

    def test_generates(self):
        a = [[1, 2], [3]]
        self.assertListEqual(list(_generator(a)), [1, 2, 3])

    def test_graph(self):
        uniques = [1, 2, 3, 4]
        as_paths = [[2, 3, 1], [4, 1, 3], [3, 4, 2]]
        G = construct_graph(uniques, as_paths)
        log.info(G)
        v = G.getVertex(1)
        self.assertIsNotNone(v)

    def test_parser_construct_graph(self):
        p = Parser(dataset="../dataset/testset")
        grp = p.graph
        print grp.getVertex(32786)
        print p.topten
        self.assertIsNotNone(grp)

    def test_compute_distances(self):

        uniques = [1, 2, 3, 4]
        as_paths = [[2, 3, 1], [4, 1], [3, 4, 2], [23, 56], [80]]
        G = construct_graph(uniques, as_paths)
        neighbor, degrees = Analyser.compute_degrees(G, as_paths)
        log.info(neighbor)
        log.info(degrees)
        self.assertIsNotNone(neighbor)

    def test_compute_transits(self):
        uniques = [1, 2, 3, 4]
        as_paths = [[2, 3, 5], [1, 4], [5, 4], [5, 2]]
        G = construct_graph(uniques, as_paths)
        neighbor, degrees = Analyser.compute_degrees(G, as_paths)
        log.info(neighbor)
        log.info(degrees)
        transits = Analyser.compute_transit_path(degrees, as_paths)
        log.info(transits)
        edges = Analyser.assign_relationship(transits, as_paths)
        log.info(edges)
        self.assertIsNotNone(neighbor)

    def test_dataset(self):
        p = Parser(dataset="../dataset/testset")
        graph = p.graph
        neighbors, degrees = Analyser.compute_degrees(graph, p.as_paths)
        transits = Analyser.compute_transit_path(degrees, p.as_paths)
        edges = Analyser.assign_relationship(transits, p.as_paths)
        log.info(edges)


