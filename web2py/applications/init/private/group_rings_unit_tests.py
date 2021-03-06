__author__ = 'LuisFontes'

import unittest
from group_rings_sec_gen_v3 import *






class FindElementInListTestCase(unittest.TestCase):

    def test_1(self):
        self.assertTrue(find_element_in_list('a', [2, 3, 'a', 4]) == 2)

    def test_1(self):
        self.assertFalse(find_element_in_list('a', [2, 3, 'a', 4]) == 3)

    def test_3(self):
        self.assertEqual(find_element_in_list('a', [2, 3, 'a', 4]), 2)

    def test_4(self):
        self.assertEqual(find_element_in_list('b', [2, 3, 'a', 4]), -1)



class GroupsTestCase(unittest.TestCase):


    def test_1(self):

        S3 = Group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])


        self.assertEqual(S3.g1 * S3.g2, S3.g2)



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
        S3 = Group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])

        self.assertTrue(S3.closed_subset([S3.g1, S3.g4, S3.g5]))




class GroupRingsTestCase(unittest.TestCase):

    def test_1(self):
        S3 = Group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])
        S3Z = GroupRing('S3Z', S3, 'Z')
        c = {S3.g1: 1, S3.g2: 1, S3.g3: 0, S3.g4: 0, S3.g5: 0, S3.g6: 0}
        d = {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6}
        gre_c = GroupRingElement(S3Z, c)
        gre_d = GroupRingElement(S3Z, d)
        product = gre_c * gre_d
        gre_a = GroupRingElement(S3Z, {S3.g1: 3, S3.g2: 3, S3.g3: 7, S3.g4: 7, S3.g5: 11,
                                                              S3.g6: 11})
        self.assertEqual(product, gre_a)

    def test_2(self):
        S3 = Group('S3', {'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'g5': 5, 'g6': 6},
               [[1, 2, 3, 4, 5, 6],
                [2, 1, 4, 3, 6, 5],
                [3, 5, 1, 6, 2, 4],
                [4, 6, 2, 5, 1, 3],
                [5, 3, 6, 1, 4, 2],
                [6, 4, 5, 2, 3, 1]])
        S3Z = GroupRing('S3Z', S3, 'Z')
        e1 = GroupRingElement(S3Z, {S3.g1: 1, S3.g2: 2, S3.g3: 3, S3.g4: 4, S3.g5: 5, S3.g6: 6})
        e2 = GroupRingElement(S3Z, {S3.g1: 6, S3.g2: 5, S3.g3: 4, S3.g4: 3, S3.g5: 2, S3.g6: 1})
        e3 = e1 * (e1 - 2 * e2) * (-1)
        resultado = GroupRingElement(S3Z, {S3.g1: -1949628, S3.g2: -1911180, S3.g3: -1853556,
                                           S3.g4: -1776756, S3.g5: -1719132, S3.g6: -1680684})

        self.assertEqual(resultado, e1 * (e2 + 7) * (e1 - 3 * e2) * e3)






if __name__ == '__main__':
    unittest.main()


