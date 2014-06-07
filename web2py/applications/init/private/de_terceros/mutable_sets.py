# groups.py
# -*- coding: utf-8 -*-


# from itertools import *



class Mset(object):
    def __init__(self, elements=[]):
        self.elements = list(set(elements))
        self.i = 0
        self.n = len(list(set(elements)))
        self.name = '{'

    def __iter__(self):
        return self
    
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return self.elements[i-1]
        else:
            raise StopIteration()

    def __str__(self):
        return self.name

        







    def issubset(self, other):
        if not isinstance(other, Mset):
            raise TypeError("One of the objects is not a Mset")
        for e in other:
            if e not in self:
                return False
        return True






a = Mset([1, 2, 3, 2])
b = Mset([1, 4, 3, 2, 7])
c = Mset([a, b])
d = Mset([a, c, 3, a, 7])

for x in d:
    print x


input()