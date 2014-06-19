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


class Group(object):
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