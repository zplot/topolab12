# groups.py
# -*- coding: utf-8 -*-

from __future__ import division
from sympy import *
import itertools



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







def find_element_in_list(element, list1):
    """
    Finds an element in a list and returns its position
    """
    try:
        index_element = list1.index(element)
        return index_element
    except ValueError:
        print '*** ERROR ****'
        return -1


class Group(object):
    def __init__(self, name, element_names, table):
        self.name = name
        self.element_names = element_names
        self.table = table
        self.string_to_int_dict = element_names
        self.int_to_string_dict = dict((v, k) for k, v in element_names.iteritems())
        tmp = {}
        for x in element_names:
            command1 = 'self.' + x + ' = GroupElement( self, "' + x + '")'
            exec command1
            command2 = 'tmp[ "' + x + '"]' + ' = GroupElement( self, "' + x + '")'
            exec command2
        self.elements = tmp
        cayley_table_names = {}
        for g1 in self.elements:
            for g2 in self.elements:
                file_n = find_element_in_list(self.string_to_int_dict[g1], self.table[0])
                column_n = find_element_in_list(self.string_to_int_dict[g2], self.table[0])
                cayley_table_names[(g1, g2)] = self.int_to_string_dict[table[file_n][column_n]]
        self.mult_table_names = cayley_table_names


        self._is_abelian = None
        self._order = None
        self._is_group = None
        self.unit = None


        if not self.is_group:
            print '*** NOT A GROUP ***'
            quit()



    @property
    def is_abelian(self):
        """
        Test if the group is Abelian
        Example:
        print 'S3.is_abelian = ', S3.is_abelian
        """
        if self._is_abelian is not None:
            return self._is_abelian

        self._is_abelian = True

        for (g1, g2) in itertools.combinations(self.elements.values(), 2):
            if g1 * g2 != g2 * g1:
                self._is_abelian = False
        return self._is_abelian

    @property
    def order(self):
        """
        Order of the group
        Example:
        print 'S3.order = ', S3.order
        """
        if self._order is not None:
            return self._order

        self._order = len(self.elements)
        return self._order

    @property
    def is_group(self):
        '''
        Test if the group is group
        '''
        if self._is_group is not None:
            return self._is_group

        self._is_group = True


        # is closed?
        for e1 in self.elements.values():
            for e2 in self.elements.values():
                if e1 * e2 not in self.elements.values():
                    self._is_group = False

        if self._is_group:
            # has unit element?
            has_unit = False
            unit = None
            for e1 in self.elements.values():
                e1_is_unit = True
                for e2 in self.elements.values():
                    if e1 * e2 != e2:
                        e1_is_unit = False
                if e1_is_unit:
                    has_unit = True
                    unit = e1
            if not has_unit:
                self._is_group = False

        if self._is_group:
            # does all elements have an inverse
            all_elements_have_inverse = True
            for e1 in self.elements.values():
                e1_has_invers = False
                for e2 in self.elements.values():
                    if e1 * e2 == unit:
                        e1_has_invers = True
                if not e1_has_invers:
                    all_elements_have_inverse = False
            if not all_elements_have_inverse:
                self._is_group = False

        if self._is_group:
            # is associative the operation
            for (e1, e2, e3) in itertools.combinations_with_replacement(self.elements.values(), 3):
                if (e1 * e2) * e3 != e1 * (e2 * e3):
                    self._is_group = False

        if self._is_group:
            self.unit = unit

        return self._is_group










class GroupElement(object):
    def __init__(self, group, name):
        self.name = name
        self.group = group
        self._inv = None

    def __mul__(self, other):
        if self.group != other.group:
            print 'NOT VALID: Groups are different'
            quit()
        result_name = self.group.mult_table_names[(self.name, other.name)]
        result = self.group.elements[result_name]
        return result

    def __str__(self):
        result = self.group.name + '.' + self.name
        return result


    @property
    def inv(self):

        if self._inv is not None:
            return self._inv

        for g in self.group.elements.values():
            if self * g == self.group.unit:
                self._inv = g
        return self._inv



class GroupRingElement(object):
    """
    coordinates is a dictionary
    group:ring es un group_ring
    """
    def __init__(self, group_ring, coordinates):
        self.coordinates = coordinates
        self.group_ring = group_ring


    def __add__(self, other):
        """
        Sum od group ring elements
        """
        result = {}
        for g in self.coordinates.keys():
            result[g] = self.coordinates[g] + other.coordinates[g]
        return result

    def __mul__(self, other):
        """
        Multiplication of group ring elements
        """
        result = {}

        for g1 in self.coordinates.keys():
            for g2 in other.coordinates.keys():

                tmp = self.coordinates[g1] * other.coordinates[g2]
                if g1 * g2 in result:
                    result[g1 * g2] = result[g1 * g2] + tmp
                else:
                    result[g1 * g2] = tmp
        result_element = GroupRingElement(self.group_ring, result)
        return result_element








    def __eq__(self, other):
        if self.group_ring != other.group_ring:
            print 'Elements belong to different group rings'
            return False
        result = True
        for x in self.coordinates:
            if self.coordinates[x] != other.coordinates[x]:
                result = False
        return result










    def __ne__(self, other):
        tmp = self == other
        return not tmp









    def __str__(self):
        """
        Nice formating for printing GroupRingElements
        """
        unordered = self.coordinates
        keys_list = []
        for x in unordered:
            keys_list.append({x.name: x})
        keys_list.sort()

        tmp = 'GroupRingElement(' + self.group_ring.name + ', '
        str_coord = '{'
        for x in keys_list:
            for x_key in x:
                str_coord = str_coord + x_key + ': ' + str(self.coordinates[x[x_key]]) + ', '
        result = tmp + str_coord[:-2] + '})'
        return result





class GroupRing(object):
    def __init__(self, name, group, ring):
        self.group = group
        self.ring = ring
        self.name = name

    def __str__(self):
        return self.name






def main():
    # global S3
    S3 = Group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])

    print
    print 'S3.g1 * S3.g2 = ', S3.g1 * S3.g2
    print 'S3.elements = ', S3.elements
    print 'S3.is_abelian = ', S3.is_abelian
    print 'S3.order = ', S3.order
    print '********************************************************'

    print 'S3.g4.inv = ', S3.g4.inv
    inverso = S3.g4.inv
    print inverso * S3.g3
    print S3.g4.inv * S3.g3

    print
    print '=================  Group Rings ========================='
    print
    a = {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6}
    b = {S3.g1: 22, S3.g2: 33, S3.g3: 44, S3.g4: 55, S3.g5: 66, S3.g6: 77}
    print 'a = ', a

    S3Z = GroupRing('S3Z', S3, 'Z')
    gre1 = GroupRingElement(S3Z, a)
    gre2 = GroupRingElement(S3Z, b)

    tmp2 = gre1 * gre2
    print
    print '******************** Probando str **********************'
    print
    print S3Z
    print tmp2
    print
    print '******************** Fin de Probando str **********************'
    print

    c = {S3.g1: 0, S3.g2: 1, S3.g3: 0, S3.g4: 0, S3.g5: 0, S3.g6: 0}
    d = {S3.g1: 22, S3.g2: 33, S3.g3: 44, S3.g4: 55, S3.g5: 66, S3.g6: 77}
    gre_c = GroupRingElement(S3Z, c)
    gre_d = GroupRingElement(S3Z, d)
    print 'gre_c = ', gre_c
    print 'gre_d = ', gre_d
    tmp3 = gre_c * gre_d
    print 'gre_c * gre_d = ', tmp3

    return










if __name__ == '__main__':
    main()









