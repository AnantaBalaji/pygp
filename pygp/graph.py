__author__ = 'AnantaBalaji'

class Vertex(object):
    def __init__(self, g, key):
        self.id = key
        self.graph = g
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight
        nbr.connectedTo[self] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getNeighbours(self):
        return set(map(lambda x: x.id, self.getConnections()))

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __iter__(self):
        return iter(self.getConnections())


class Graph(object):
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(self, key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def get(self, key):
        return self.vertList.get(key)

def map_paths(graph, as_path):

    for index, element in enumerate(as_path):
        # print index, element, len(as_path)
        if index+1 >= len(as_path):
            break
        graph.addEdge(element, as_path[index+1])


def construct_graph(uniques, as_paths):

    G = Graph()
    print uniques
    print as_paths

    for key in uniques:
        G.addVertex(key=key)

    for path in as_paths:
        map_paths(G, path)

    return G