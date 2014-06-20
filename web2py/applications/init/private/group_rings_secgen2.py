# group_rings_secgen.py
# -*- coding: utf-8 -*-

from __future__ import division
# from sympy.ntheory import factorint
import itertools
from math_sets import *
from copy import deepcopy as deepcopy


# Para logging en este módulo. Descomentar filename para hacer logging al fichero
import logging

logging.basicConfig(
    # filename="../private/modulo53.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filemode='w',
    level=logging.INFO
)

traza = logging.getLogger(__name__)








def group_element(name, group):

    class GroupElement(object):

        def __init__(self, group, name):
            self.name = name
            self.group = group


    # return GroupElement(group, name)
    return group(name)







def group(name, element_names_sit, table_dic):
    """
    Finite groups class.
    Example:
    S3 = Group('S3', Sit(['g1', 'g2', 'g3', 'g4', 'g5', 'g6']),

                {(g1, g1): g1,
                 (g1, g2): g2,
                 .
                 .
                 .
                 .............})

    """

    class Group(object):

        def __init__(self, name, element_names_sit, table_dic):
            self.name = name
            self.element_names_sit = element_names_sit
            self.table = table_dic

        def __call__(self, a):
            return a

    return Group(name, element_names_sit, table_dic)




def main():


    S3 = group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])

    print S3.name
    print S3(4)


    elemento = group_element('g1', S3)
    print elemento








    return










if __name__ == '__main__':
    main()