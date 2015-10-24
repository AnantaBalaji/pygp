# coding=utf-8
__author__ = 'plasmashadow'

class Analyser(object):

    @classmethod
    def compute_degrees(cls, graph, as_paths):
        """
         Takes in the graph object and apply gao algorithm to
         compute distance between n nodes.
         Compute the degree for each AS
            for each AS path (u1, u2, ..., un) in routing tables do
                   for each i = 1, ..., n − 1 do
                      neighbor[ui] = neighbor[ui] ∪ {ui+1}
                      neighbor[ui+1] = neighbor[ui+1] ∪ {ui}
                   end for
            end for
            for each AS u do
                    degree[u] = |neighbor[u]|
            end for
        """
        neighbors = {}
        degree = {}

        for path in as_paths:
            for index, key in enumerate(path):
                if index+1 >= len(path):
                    break
                v1 = graph.get(key)
                v2 = graph.get(path[index+1])
                neighbors[key] = v1.getNeighbours() | v2.getNeighbours()
                neighbors[path[index+1]] = v2.getNeighbours() | v1.getNeighbours()

        for key in neighbors:
            degree[key] = len(neighbors[key])

        return neighbors, degree

    @classmethod
    def compute_transit_path(cls):
        pass





