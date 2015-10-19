__author__ = 'AnantaBalaji'

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import six,copy
import logging
from .graph import construct_graph


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _generator(lists):
    """flattens the list"""
    for x in lists:
        if isinstance(x, (list, set)):
            for i in x:
                yield i
        else:
            yield x

def _generate(sets, buffer):
    """Copies the sets to a string buffer object"""
    for sublist in sets:
        sublist = map(str, sublist)
        buffer.write(" ".join(sublist))
        buffer.write("\n")
    return buffer

def _intersection(seq):
    """ Removes Duplicates without changing the order"""
    prev = None
    res_seq = []
    for e in seq:
        if e == prev:
            continue
        prev = e
        res_seq.append(e)
    return res_seq



def _process_path(as_path):
    """
     Takes in a path and splits
     it into key and value

     for example:
       201 34 56 789  is transformed to
      4, [201, 34, 56, 789]

    """
    entry_list = as_path.split()
    values = map(long, entry_list)
    return values


def preprocess_dataset(as_paths):
    """
     Inorder to preprocess the data group the value by its size
     and  for each larger set check there exist a smaller set
     with in it.

     Args: (str) path data
    """
    result_list = []
    dump_list = []
    for path in as_paths:
        value = _process_path(path)
        _repeated = False
        for val in result_list:
            if set(val).issubset(set(value)):
                _repeated = True
        if not _repeated:
            result_list.append(_intersection(value))

    l = result_list
    l2 = l[:]
    for m in l:
        for n in l:
            if set(m).issubset(set(n)) and m != n:
                l2.remove(m)
                break

    return l2, set(list(_generator(l2)))

def map_filter(as_paths):
    """
    Considering the a as_set (a,b,c)
    where a, b, c are the nodes of the
    set.
    1) should discard all as_set which contains
       another as_set in it.
    2) should compress all as_sets in which
       an node is repeated.
    3) duplicate path should also be removed

    Args:
      as_paths:list(str) on destfile.

    returns:
      valid dataset buffer
    """
    processed_values, uniques = preprocess_dataset(as_paths)
    processed_values = list(processed_values)
    buffer = StringIO()
    _generate(processed_values, buffer)
    return buffer, uniques, processed_values


class Parser(object):
    """
    Parser Object is used to parse the dataset
    from the given as maps.
    """

    map_filter = staticmethod(map_filter)

    def __init__(self, dataset=None):
        if not dataset:
            self.data = open("../dataset/destfile", "r").read()
        else:
            self.data = open(dataset, "r").read()
        self.parsed_data = self.data.split("\n")
        self.parsed_data.pop()
        self.as_paths = map(lambda x: x.split(":")[1] or x, self.parsed_data)
        self.actual_values, self.uniques, self.as_paths = Parser.map_filter(self.as_paths)
        self.as_graph = None

    def generate_path(self, destination, filename=None):
        if not filename:
            filename = "destset"
        filename = destination + "/"+filename
        f = open(filename, "w+")
        f.write(self.actual_values.getvalue())

    def __construct_graph(self):
        self.as_graph = construct_graph(self.uniques, self.as_paths)

    @property
    def graph(self):
        self.__construct_graph()
        return self.as_graph

    @property
    def topten(self):
        graph = six.iteritems(self.as_graph.vertList)
        items = sorted(graph, key=lambda x: len(list(six.iterkeys(x[1].connectedTo))))
        return map(lambda x: x[1].id,items[:10])