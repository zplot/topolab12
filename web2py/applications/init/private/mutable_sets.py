# groups.py
# -*- coding: utf-8 -*-


# from itertools import *



class Mset(object):
    """
    Mset models generalized sets. Msets are mutable
    """
    def __init__(self, elements=[]):
        self._elements = list(set(elements))
        self.i = 0
        # self.n = len(self._elements)

    @property
    def n(self):
        return len(self._elements)

    @property
    def name(self):
        name = []
        for x in self._elements:
            if isinstance(x, Mset):
                name.append(x.name)
            else:
                name.append(x)
        return name


    def __iter__(self):
        self.i = 0
        return self
    
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return self._elements[i-1]
        else:
            raise StopIteration()

    def __str__(self):
        return str(self.name)

    @property
    def elements(self):
        return str(self)

    def append(self, other):
        self._elements.append(other)
        self._elements = list (set(self._elements))
        return





    def is_subset(self, other):
        if not isinstance(other, Mset):
            raise TypeError("One of the objects is not a Mset")
        for e in other:
            if e not in self:
                return False
        return True






a = Mset([1, 2, 'joe', 2])
b = Mset([1, 4, 3, 2, 7])
c = Mset([a, b])
d = Mset([a, c, 3, a, 7])

print a
print b
print c
print d
print d
print d.elements


for x in d:
    print x

print ' ******* Probamos append ****************'
print
a.append(11)
a.append(11)
a.append(11)
a.append(11)
print a

print ' ******* Probamos iterator ****************'
print
for x in a:
    print x

for x in a:
    print x

print ' ******* Probamos is_element ****************'
print
print 1 in a
print 'joe' in a
print a
print c in d
print b in d
print a in d

