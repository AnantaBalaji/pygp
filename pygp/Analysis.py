# coding=utf-8
__author__ = 'plasmashadow'

def find_nodes(degrees, paths):
    """
      Find the node degrees with
      nodes of the given path.
    """
    path_degrees = map(lambda x: degrees[x], paths)

    min_val = min(path_degrees, key=lambda x: x)

    max_val = max(path_degrees, key=lambda x: x)

    j_min = filter(lambda x: degrees.get(x, 0) == min_val, paths)[0]
    j_max = filter(lambda x: degrees.get(x, 0) == max_val, paths)[0]
    j_min, j_max = paths.index(j_min), paths.index(j_max)
    return j_min, min_val, j_max, max_val



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
                neighbors[key] = v1.getNeighbours() | set([path[index+1]])
                neighbors[path[index+1]] = v2.getNeighbours() | set([key])

        for key in neighbors:
            degree[key] = len(neighbors[key])

        return neighbors, degree

    @classmethod
    def compute_transit_path(cls, degree, as_paths):
        """
            Count the number of routing table entries that infer
            an AS pair having a transit relation-ship

             for each AS path (u1, u2, ..., un) do
             find the smallest j such that degree[uj ] = max1≤i≤ndegree[ui]
                 for i = 1, ..., j − 1 do
                    transit[ui, ui+1] = transit[ui, ui+1] + 1
                 end for
                 for i = j, ..., n − 1 do
                    transit[ui+1, ui] = transit[ui+1, ui] + 1
                 end for
             end for
        """
        transits = {}
        for path in as_paths:
            if len(path) == 1:
                continue
            j_min, min_val, j_max, max_val = find_nodes(degree, path)
            for index, element in enumerate(path):
                if index+1 >= len(path):
                    break
                next_element = path[index+1]
                if index < j_min:
                    key = (element, next_element)
                    transits[key] = transits.get(key, 0) + 1
                else:
                    key = (next_element, element)
                    transits[key] = transits.get(key, 0) + 1
        return transits

    @classmethod
    def assign_relationship(cls, transits, as_paths):
        """
        Compute all as relationship

        for each AS path (u1, u2, ..., un) do
            for i = 1, ..., n − 1 do
                if (transit[ui+1, ui] > L and transit[ui, ui+1] > L)
                             or (transit[ui, ui+1] ≤ L and transit[ui, ui+1] > 0
                             and transit[ui+1, ui] ≤ L and transit[ui+1, ui] > 0) then
                edge[ui, ui+1] = sibling-to-sibling
                else if transit[ui+1, ui] > L or transit[ui, ui+1] = 0 then
                edge[ui, ui+1] = provider-to-customer
                else if transit[ui, ui+1] > L or transit[ui+1, ui] = 0 then
                edge[ui, ui+1] = customer-to-provider
                end if
            end for
        end for
        """
        L = 1
        edges = {}
        for path in as_paths:
            if len(path) == 1:
                continue
            for index, element in enumerate(path):
                if index+1 >= len(path):
                    break
                next_element = path[index+1]
                if transits.get((next_element, element)) > L and transits.get((element, next_element)) > L \
                           or (transits.get((next_element, element)) <= L and transits.get((element, next_element)) > 0 \
                           and transits.get((next_element, element)) <= L and transits.get((element, next_element)) > 0):

                    key = (element, next_element)
                    edges[key] = "SIBLING-TO-SIBLING"
                elif transits.get((next_element, element)) > L or transits.get((element, next_element)) == 0:
                    key = (element, next_element)
                    edges[key] = "PROVIDER-TO-CUSTOMER"
                elif transits.get((element, next_element)) > L or transits.get((element, next_element)) == 0:
                    key = (element, next_element)
                    edges[key] = "CUSTOMER-TO-PROVIDER"
        return edges