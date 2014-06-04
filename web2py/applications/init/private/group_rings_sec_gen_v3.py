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
        print '*** Element not in the list ****'
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
        self._unit = None

        if self.is_group:
            self.is_a_group_at = True
        else:
            self.is_a_group_at = False
            print
            print '********************* is not a group **************************'
            print





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

        es_un_grupo = True


        # is closed?
        for e1 in self.elements.values():
            for e2 in self.elements.values():
                if e1 * e2 not in self.elements.values():
                    es_un_grupo = False

        if es_un_grupo:
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
                es_un_grupo = False

        if es_un_grupo:
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
                es_un_grupo = False

        if es_un_grupo:
            # is associative the operation
            for (e1, e2, e3) in itertools.combinations_with_replacement(self.elements.values(), 3):
                if (e1 * e2) * e3 != e1 * (e2 * e3):

                    es_un_grupo = False
        print
        if es_un_grupo:
            self.unit = unit


        return es_un_grupo






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

    def __eq__(self, other):
        result = self.name == other.name
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
        return self._inv



class GroupRingElement(object):
    """
    coordinates is a dictionary
    group:ring es un group_ring
    """
    def __init__(self, group_ring, coordinates):
        self.coordinates = coordinates
        self.group_ring = group_ring


        unordered = self.coordinates
        keys_list = []
        for x in unordered:
            keys_list.append({x.name: x})
        keys_list.sort()

        tmp = 'GroupRingElement(' + self.group_ring.name + ', '
        str_coord = '{'
        for x in keys_list:
            for x_key in x:
                str_coord = str_coord + x[x_key].group.name + '.' + x_key + ': ' + str(self.coordinates[x[x_key]]) + \
                            ', '
        result = tmp + str_coord[:-2] + '})'
        self.name = result



    def __add__(self, other):
        """
        Sum od group ring elements
        """
        if isinstance(other, GroupRingElement):
            result = {}
            for g in self.coordinates.keys():
                tmp = self.coordinates[g] + other.coordinates[g]
                result[g] = tmp
            result_element = GroupRingElement(self.group_ring, result)
            return result_element
        elif isinstance(other, int):
            result = {}
            for g in self.coordinates.keys():
                if g == self.group_ring.group.unit:
                    tmp = self.coordinates[g] + other
                else:
                    tmp = self.coordinates[g]
                result[g] = tmp
            result_element = GroupRingElement(self.group_ring, result)
            return result_element


    def __radd__(self, other):
        """
        Multiplication of group ring elements when the left operand is not a group ring element
        """
        return self + other



    def __sub__(self, other):
        """
        Sum od group ring elements
        """
        if isinstance(other, GroupRingElement):
            result = {}
            for g in self.coordinates.keys():
                tmp = self.coordinates[g] - other.coordinates[g]
                result[g] = tmp
            result_element = GroupRingElement(self.group_ring, result)
            return result_element
        elif isinstance(other, int):
            result = {}
            for g in self.coordinates.keys():
                if g == self.group_ring.group.unit:
                    tmp = self.coordinates[g] - other
                else:
                    tmp = self.coordinates[g]
                result[g] = tmp
            result_element = GroupRingElement(self.group_ring, result)
            return result_element




    def __rsub__(self, other):
        """
        Multiplication of group ring elements when the left operand is not a group ring element
        """
        return (self - other) * -1








    def __mul__(self, other):
        """
        Multiplication of group ring elements
        """

        if isinstance(other, GroupRingElement):
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
        elif isinstance(other, int):
            result = {}
            for g in self.coordinates.keys():
                tmp = self.coordinates[g] * other
                result[g] = tmp
            result_element = GroupRingElement(self.group_ring, result)
            return result_element
        else:
            print '********* Houston, we have a problem'
            quit()

    def __rmul__(self, other):
        """
        Multiplication of group ring elements when the left operand is not a group ring element
        """
        return self * other








    def __eq__(self, other):

        result = self.name == other.name
        return result


    def __ne__(self, other):
        tmp = self == other
        return not tmp


    def __str__(self):
        """
        Nice formating for printing GroupRingElements
        """
        return self.name





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
    aa = S3.g1 * S3.g2
    ab = S3.g2
    print 'aa==ab = ', aa == ab
    print S3.g1 * S3.g2 == S3.g2
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



    print '***************** Quaternions ***************************'
    print
    Q8 = Group('Q8', {'one': 1, 'minus_1': 2, 'i': 3, 'minus_i': 4, 'j': 5, 'minus_j': 6, 'k': 7, 'minus_k': 8},
           [[1, 2, 3, 4, 5, 6, 7, 8],
            [2, 1, 4, 3, 6, 5, 8, 7],
            [3, 4, 2, 1, 8, 7, 5, 6],
            [4, 3, 1, 2, 7, 8, 6, 5],
            [5, 6, 7, 8, 2, 1, 4, 3],
            [6, 5, 8, 7, 1, 2, 3, 4],
            [7, 8, 6, 5, 3, 4, 2, 1],
            [8, 7, 5, 6, 4, 3, 1, 2]])
    print 'Q8.elements = ', Q8.elements
    print 'Q8.is_abelian = ', Q8.is_abelian
    print 'Q8.order = ', Q8.order
    print 'Q8.is_group = ', Q8.is_group
    print
    print
    print '=================  Group Rings ========================='
    print
    a = {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6}
    b = {S3.g1: 22, S3.g2: 33, S3.g3: 44, S3.g4: 55, S3.g5: 66, S3.g6: 77}


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
    c = {S3.g1: 1, S3.g2: 1, S3.g3: 0, S3.g4: 0, S3.g5: 0, S3.g6: 0}
    d = {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6}
    gre_c = GroupRingElement(S3Z, c)
    gre_d = GroupRingElement(S3Z, d)
    print 'gre_c = ', gre_c
    print 'gre_d = ', gre_d
    tmp3 = gre_c * gre_d
    print 'gre_c * gre_d = ', tmp3
    print
    print '**************************** GroupRingElements por números enteros *************************'
    print
    ge = GroupRingElement(S3Z, {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6})
    dos = GroupRingElement(S3Z, {S3.g1: 2, S3.g2: 0, S3.g3: 0, S3.g4: 0, S3.g5: 0, S3.g6: 0})
    hola = dos + ge
    print 'hola = ', hola.name
    hola_menos = dos - ge
    print 'hola_menos = ', hola_menos.name

    suma = ge * 2
    print ge
    print suma
    amus = 2 * ge
    print amus
    print
    print '*********************** Suma de Enteros y GroupRing Elements ******************'
    print
    print ge
    print dos
    print ge + dos
    print ge + 2
    print 2 + ge
    print '*********************** Probando cosas raras ******************'
    print
    e1 = GroupRingElement(S3Z, {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6})
    e2 = GroupRingElement(S3Z, {S3.g1: 6, S3.g2: 5, S3.g3: 4, S3.g4: 3, S3.g5: 2, S3.g6: 1})
    print e1
    print e2
    print e1 + e2
    print e1 - 2 * e2
    print e1 - 2
    print 2 - e1
    print
    print (2 + ge) * 4
    e3 = e1 * (e1 - 2 * e2) * (-1)
    print e3
    print e1 * (e2 + 7) * (e1 - 3 * e2) * e3
    print '.............'
    e3 = e1 * (e1 - 2 * e2) * (-1)
    print e3
    print 'probamos git 09:21'







    return










if __name__ == '__main__':
    main()










