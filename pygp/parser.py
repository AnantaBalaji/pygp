__author__ = 'AnantaBalaji'

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import collections
import logging
from .graph import construct_graph
from .Analysis import Analyser


class OrderedSet(collections.Set):
    """
      Used to preserve the elements while set
      operation.
    """

    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)

    def __len__(self):
        return len(self.d)

    def __contains__(self, element):
        return element in self.d

    def __iter__(self):
        return iter(self.d)

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

def ordered_intersection(list1, list2):
    return [x for x in list1 if x in list2]



def _process_path(as_path, duplicate=False):
    """
     Takes in a path and splits
     it into key and value

     for example:
       201 34 56 789  is transformed to
      4, [201, 34, 56, 789]

    """
    if duplicate:
        as_path = reduce(lambda x, y: x + y.lstrip(), re.split("{.*}", as_path))
    as_path = as_path.lstrip()
    entry_list = as_path.split()
    values = map(long, entry_list)
    return values

def has_dulicate(lists):
    dst = dict.fromkeys(lists)
    if len(dst.keys()) < len(lists):
        return True
    return False

from collections import OrderedDict

def remove_duplicates(lists):

    dst = OrderedDict.fromkeys(lists)
    return dst.keys()



# def _preprocess_dataset(as_paths):
#     """
#      Inorder to preprocess the data group the value by its size
#      and  for each larger set check there exist a smaller set
#      with in it.
#
#      Args: (str) path data
#     """
#     result_list = []
#     dump_list = []
#     for path in as_paths:
#         value = _process_path(path)
#         print "Value ==", value
#         if not value:
#             continue
#         _repeated = False
#         res = value
#         for val in result_list:
#             print val, value
#             if OrderedSet(value).issubset(val):
#                 print "is subset"
#                 res = OrderedSet(val) - OrderedSet(value)
#                 print res
#             elif OrderedSet(value).issuperset(val):
#                 print "is superset"
#                 res = OrderedSet(value) - OrderedSet(val)
#                 print res
#         result_list.append(res)
#
#     l = result_list
#     l2 = l[:]
#     for m in l:
#         for n in l:
#             if set(m).issubset(set(n)) and m != n:
#                 l2.remove(m)
#                 break
#
#     return l2, set(list(_generator(l2)))

import re

def preprocess_dataset(as_paths):

    regex_compile = re.compile(r'{(.*)}')
    pre_processed_path = []
    for path in as_paths:
        path_group = regex_compile.search(path)
        if not path_group:
            value = _process_path(path, duplicate=False)
            if remove_duplicates(value) not in pre_processed_path:
                pre_processed_path.append(remove_duplicates(value))
        else:

            groups,  = path_group.groups()
            if not len(groups.split(",")) > 1:
                value = _process_path(path, duplicate=True)
                against = map(lambda x: long(x.strip()), groups.split(","))
                if against.pop() not in value:
                    pre_processed_path.append(remove_duplicates(value))

    return pre_processed_path, set(list(_generator(pre_processed_path)))




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
        self.as_paths = map(lambda x: x.split(":")[1] if x != "" else x, self.parsed_data)

        self.actual_values, self.uniques, self.as_paths = Parser.map_filter(self.as_paths)
        self.as_graph = None

    def generate_path(self, destination, filename=None):
        """
        Writes a processed as_graph into a
        file.
        """
        if not filename:
            filename = "destset"
        filename = destination + "/"+filename
        f = open(filename, "w+")
        f.write(self.actual_values.getvalue())

    def __construct_graph(self):
        """constructs the as graph"""
        self.as_graph = construct_graph(self.uniques, self.as_paths)

    @property
    def graph(self):
        """
        Construct as_graph with as_paths.
        """
        self.__construct_graph()
        return self.as_graph

    @property
    def topten(self):
        """
        Computes the top 10 nodes in the unprocessed graph
        with highest degrees.
        """
        graph = self.as_graph.vertList.items()
        items = sorted(graph, key=lambda x: len(x[1].connectedTo.keys()), reverse=True)
        return map(lambda x: x[1].id, items[:10])

    def compute_degrees_and_neighbors(self):
        """
          Computes the degree and neighbours of
          each nodes in AS GRAPH thought
          gao algorithm.
        """
        return Analyser.compute_degrees(self.as_graph, self.as_paths)