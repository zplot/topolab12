__author__ = 'LuisFontes'

import unittest
from math_sets import *






class SitsTestCase(unittest.TestCase):


    def test_nested_sets_1(self):

        a = Sit([1, 2, 3])
        b = Sit([3, 4, a])
        c = Sit([1, 4, a, b])

        self.assertEqual(c, Sit([Sit([3, 1, 2]), 1, 4, Sit([4, Sit([3, 1, 2]), 3])]))

    def test_nested_sets_2(self):

        a = Sit([])
        b = Sit([3, 4, a])
        c = Sit([1, 4, a, b])

        self.assertEqual(c, Sit([Sit([Sit([]), 4, 3]), 1, 4, Sit([])]))

    def test_order_does_not_matter_1(self):

        a = Sit([1, [2, 3, [4, 5, 6]]])

        self.assertEqual(a, Sit([[2, 3, [4, 5, 6]], 1]))

    def test_order_does_not_matter_2(self):

        a = Sit([1, [2, 'this is a string', [4, 5, 6]]])

        self.assertEqual(a, Sit([[2, 'this is a string', [4, 5, 6]], 1]))

    def test_order_does_not_matter_3(self):

        a = Sit([1, 2, 3, 4, 5])
        b = Sit([1, 3, 5, 4, 2])

        self.assertEqual(a, b)

    def test_cardinal_1(self):

        a = Sit([1, [2, 3, [4, 5, 6]]])

        self.assertEqual(a.len, 2)

    def test_cardinal_2(self):

        a = Sit([1, 3, '4', 9, '4', 3, 1, Sit([])])

        self.assertEqual(a.len, 5)

    def test_cardinal_3(self):

        a = Sit([])

        self.assertEqual(a.len, 0)

    def test_iterator_1(self):

        a = Sit([1, 2, 3, 4, 5, 6, 7])
        b = Sit([])
        for x in a:
            b.add(x)

        self.assertEqual(a, b)

    def test_eq_1(self):

        a = Sit([1, 2, 3, 4, 5, 6, 7])
        b = Sit([5, 3, 1, 2, 4, 7, 6])

        self.assertEqual(a, b)

    def test_issubset_1(self):

        a = Sit([1, 2, 3, 4, 5, 6, 7])
        b = Sit([2,4,6])

        self.assertTrue(a.issubset(b))






"""
    def test_2(self):
        Q8 = Group('Q8', {'one': 1, 'minus_1': 2, 'i': 3, 'minus_i': 4, 'j': 5, 'minus_j': 6, 'k': 7, 'minus_k': 8},
                   [[1, 2, 3, 4, 5, 6, 7, 8],
                    [2, 1, 4, 3, 6, 5, 8, 7],
                    [3, 4, 2, 1, 8, 7, 5, 6],
                    [4, 3, 1, 2, 7, 8, 6, 5],
                    [5, 6, 7, 8, 2, 1, 4, 3],
                    [6, 5, 8, 7, 1, 2, 3, 4],
                    [7, 8, 6, 5, 3, 4, 2, 1],
                    [8, 7, 5, 6, 4, 3, 1, 2]])

        self.assertTrue(Q8.is_group)


    def test_3(self):
        Q8Falso = Group('Q8', {'one': 1, 'minus_1': 2, 'i': 3, 'minus_i': 4, 'j': 5, 'minus_j': 6, 'k': 7,
                               'minus_k': 8},
           [[1, 2, 3, 4, 5, 6, 7, 8],
            [2, 1, 4, 3, 6, 5, 8, 7],
            [3, 4, 2, 1, 8, 7, 5, 6],
            [4, 3, 1, 2, 7, 8, 6, 5],
            [5, 6, 7, 8, 2, 1, 4, 3],
            [6, 5, 8, 7, 1, 2, 3, 4],
            [7, 8, 6, 5, 3, 4, 2, 1],
            [5, 7, 5, 6, 4, 3, 1, 2]])

        self.assertFalse(Q8Falso.is_group)

    def test_4(self):
        Sit3 = Group('Sit3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])

        self.assertTrue(Sit3.closed_subset([Sit3.g1, Sit3.g4, Sit3.g5]))




class GroupRingsTestCase(unittest.TestCase):

    def test_1(self):
        Sit3 = Group('Sit3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])
        Sit3Z = GroupRing('Sit3Z', Sit3, 'Z')
        c = {Sit3.g1: 1, Sit3.g2: 1, Sit3.g3: 0, Sit3.g4: 0, Sit3.g5: 0, Sit3.g6: 0}
        d = {Sit3.g1: 1, Sit3.g2: 2, Sit3.g3: 3, Sit3.g4: 4, Sit3.g5: 5, Sit3.g6: 6}
        gre_c = GroupRingElement(Sit3Z, c)
        gre_d = GroupRingElement(Sit3Z, d)
        product = gre_c * gre_d
        gre_a = GroupRingElement(Sit3Z, {Sit3.g1: 3, Sit3.g2: 3, Sit3.g3: 7, Sit3.g4: 7, Sit3.g5: 11,
                                                              Sit3.g6: 11})
        self.assertEqual(product, gre_a)

    def test_2(self):
        Sit3 = Group('Sit3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])
        Sit3Z = GroupRing('Sit3Z', Sit3, 'Z')
        e1 = GroupRingElement(Sit3Z, {Sit3.g1: 1, Sit3.g2: 2, Sit3.g3: 3, Sit3.g4: 4, Sit3.g5: 5, Sit3.g6: 6})
        e2 = GroupRingElement(Sit3Z, {Sit3.g1: 6, Sit3.g2: 5, Sit3.g3: 4, Sit3.g4: 3, Sit3.g5: 2, Sit3.g6: 1})
        e3 = e1 * (e1 - 2 * e2) * (-1)
        resultado = GroupRingElement(Sit3Z, {Sit3.g1: -1949628, Sit3.g2: -1911180, Sit3.g3: -1853556,
                                           Sit3.g4: -1776756, Sit3.g5: -1719132, Sit3.g6: -1680684})

        self.assertEqual(resultado, e1 * (e2 + 7) * (e1 - 3 * e2) * e3)
"""





if __name__ == '__main__':
    unittest.main()


