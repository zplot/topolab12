# mutable_sets.py
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


    def __eq__(self, other):
        if not isinstance(other, Mset):
            return False
        result = True
        for e1 in self._elements:
            if e1 not in other._elements:
                result = False
        for e1 in other._elements:
            if e1 not in self._elements:
                result = False
        return result



    
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





    def issubset(self, other):
        if not isinstance(other, Mset):
            raise TypeError("One of the objects is not a Mset")
        for e in other:
            if e not in self:
                return False
        return True

    def issuperset(self, other):
        if not isinstance(other, Mset):
            raise TypeError("One of the objects is not a Mset")
        for e in self:
            if e not in other:
                return False
        return

    def union(self, other):
        tmp = list(set(self._elements) | set(other._elements))
        result = Mset(tmp)
        return result

    def intersection(self, other):
        tmp = list(set(self._elements) & set(other._elements))
        result = Mset(tmp)
        return result

    def difference(self, other):
        tmp = list(set(self._elements) - set(other._elements))
        result = Mset(tmp)
        return result

    def symmetric_difference(self, other):
        tmp = list(set(self._elements) ^ set(other._elements))
        result = Mset(tmp)
        return result








a = Mset([1, 2, 'joe', 2])
b = Mset([1, 4, 3, 2, 7])
c = Mset([a, b])
d = Mset([a, c, 3, a, 7])
e = Mset([a, c])

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

print ' ******* Probamos is element ****************'
print
print 1 in a
print 'joe' in a
print a
print c in d
print b in d
print a in d

print ' ******* Probamos issubset ****************'
print d
print a
print d.issubset(a)
print d.issubset(e)
print d.issubset(Mset([a, 3]))

print ' ******* Probamos issuperset ****************'
print d
print e
print e.issuperset(d)
print d.issuperset(e)

print ' ******* Probamos union ****************'
print d
print e
print e.union(d)
print d.union(e)
print e.union(d) == e.union(d)
f = Mset([1, 2])
print f
print f.union(e)

print ' ******* Probamos intersección ****************'
print c
print d
print c.intersection(d)
print Mset([1, 2, 3, 4, 5]).intersection(Mset([4, 5, 6, 7]))
g = Mset([1, 2, 3, 4, 5]).intersection(Mset([4, 5, 6, 7]))
print g
print isinstance(g, Mset)
print g == Mset([4, 5])
print g == Mset([4, 5, 4, 4, 5])

