# modulo53_v5.py
# -*- coding: utf-8 -*-

# Ficheros que dependen de este: matplotlib


import itertools
import networkx as nx

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


class Set(object):
    # El conjunto sólo debe crearse si está bien formado
    def __init__(self, conjunto):
        """


        """
        self.theElements = conjunto
        self.index = 0

    #def __str__(self):

    # Determines if an element is in the set.
    def __contains__(self, element):
        return element in self.theElements

    # Nuevo iterator
    def __iter__(self):
        return self

    def next(self):
        try:
            result = self.theElements[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    # Returns the number of items in the set.
    def __len__(self):
        return len(self.theElements)

    # Adds a new unique element to the set.
    def add(self, element):
        if element not in self:
            self.theElements.append(element)


    # Removes an element from the set.
    def remove(self, element):
        assert element in self, "The element must be in the set."
        self.theElements.remove(element)

    # Determines if two sets are equal.
    def __eq__(self, setB):
        if isinstance(setB, Set):
            if len(self) != len(setB):
                return False
            else:
                return self.isSubsetOf(setB)
        else:
            return False

    # Determines if this set is a subset of setB.
    def isSubsetOf(self, setB):
        for elem in self.theElements:
            if elem not in setB.theElements:
                return False
        return True

    # Creates a new set from the union of this set and setB.
    def union(self, setB):
        newSet = Set()
        newSet.theElements.extend(self.theElements)
        for element in setB:
            if element not in self:
                newSet.theElements.append(element)
        return newSet

    #Creates a new set from the intersection: self set and setB.
    def interset(self, setB):
        resultado = Set()
        for elem in self.theElements:
            if elem in setB:
                resultado.add(elem)
        return resultado


    # Creates a new set from the difference: self set and setB.
    def difference(self, setB):
        resultado = Set()
        for elem in self.theElements:
            if elem not in setB:
                resultado.add(elem)
        return resultado


    # Power set
    def powerset(self):
        tmp1 = Set([])
        for i in powersetgen(self.theElements):
            tmp1.add(i)
        return tmp1


class Topo(object):
    '''
    Esta clase modela espacios topológicos. Tiene puntos, abiertos, aristas y abiertos mínimos y más cosas

    '''


    def __init__(self, puntos, abiertos):
        # Nos salimos si no es espacio o si no es T0
        traza.info('Entro en la clase Topo')
        if not es_espacio_topologico(puntos, abiertos):
            traza.info('Sorry, it is not a topological space')
            traza.info('Cortamos y salimos')
            exit()
        if not es_t0(puntos, abiertos):
            traza.info('Sorry, this space is not T0')
            traza.info('Cortamos y salimos')
            exit()

        self.puntos = puntos
        self.abiertos = abiertos
        self.aristas = []
        self.Mx = dict()
        for punto in self.puntos:
            conj1 = Set([])
            for abierto in self.abiertos:
                if punto in abierto:
                    conj1.add(abierto)
            self.Mx[punto] = intersec(conj1.theElements)
        aristastmp = []
        for punto1 in puntos:
            for punto2 in puntos:
                if punto1 in self.Mx[punto2]:
                    if punto1 <> punto2:
                        aristastmp.append([punto1, punto2])
        for arista in aristastmp:
            hay_punto_en_medio = False
            ponemos_la_arista = True
            hay_un_ciclo = False
            punto_bajo = arista[0]
            punto_alto = arista[1]
            for punto in puntos:
                # ¿Está el punto en medio de la arista?
                if [punto_bajo, punto] in aristastmp and [punto, punto_alto] in aristastmp:
                    hay_punto_en_medio = True
                # ¿Hay un ciclo entre punto alto y punto bajo?
                if [punto_bajo, punto_alto] in aristastmp and [punto_alto, punto_bajo] in aristastmp:
                    hay_un_ciclo = True

                if hay_punto_en_medio and not hay_un_ciclo:
                    ponemos_la_arista = False
            if ponemos_la_arista:
                self.aristas.append(arista)

        G1 = nx.DiGraph()
        G1.add_nodes_from(self.puntos)
        G1.add_edges_from(self.aristas)
        # Cálculo de los elementos mínimos. Son aquellos que no tienen ningún punto por debajo
        elementos_minimos = []
        for punto1 in G1.nodes():
            hay_punto_por_abajo = False
            for punto2 in G1.nodes():
                if punto1 <> punto2:
                    if nx.has_path(G1, source=punto2, target=punto1):
                        hay_punto_por_abajo = True
            if not hay_punto_por_abajo:
                elementos_minimos.append(punto1)

        # Ahora vamos a preparar un procedimiento no-recursivo para ir asignando rango a los diferentes
        # elementos de acuerdo con el criterio de E. W.: rank[x] = max { rank(y) +1 : y < x }



        # Cálculo de los niveles que tiene el grafo
        niveles = 0
        for punto1 in G1.nodes():
            for punto2 in G1.nodes():
                if nx.has_path(G1, source=punto1, target=punto2):
                    longitud = nx.shortest_path_length(G1, source=punto1, target=punto2)
                    if longitud > niveles:
                        niveles = longitud
        niveles = niveles + 1


        # Vamos a asignar rank a cada punto
        rank = {}
        for x in elementos_minimos:
            rank[x] = 0

        # Ya tienen rango asignado las elementos de nivel 0

        # Vamos con el nivel i desde i = 1 hasta niveles-1

        for i in range(1, niveles + 1):
            for y in G1.nodes():
                for x in rank.keys():
                    if rank[x] == i - 1:
                        if nx.has_path(G1, source=x, target=y):
                            longitud = nx.shortest_path_length(G1, source=x, target=y)
                            if longitud == 1:
                                rank[y] = i



        # Ahora pasamos del diccionario rank al diccionario nivel, donde para cada nivel
        # tenemos los puntos que están en él.

        nivel = {}
        for i in range(0, niveles):
            nivel[i] = []
        for key in rank:
            a = rank[key]
            b = key
            nivel[a].append(b)

        # anchura del diagrama de hasse
        anchura = 0
        for i in nivel:
            if len(nivel[i]) > anchura:
                anchura = len(nivel[i])

        pos = {}
        for key in nivel:
            ancho_del_nivel = len(nivel[key])
            blancos_izda = (anchura - ancho_del_nivel) // 2
            x_anterior = blancos_izda
            for punto in nivel[key]:
                x = x_anterior + 1
                x_anterior = x
                pos[punto] = (x, key)

        mapa1 = Mapa(pos, self.aristas)
        mapa2 = optimo(mapa1)

        # cogemos las posiciones del mapa óptimo
        pos_optima = mapa2.pos
        self.pos_optima = pos_optima




        # Ahora le ponemos etiquetas de los nodos
        labels = {}
        for i in self.puntos:
            labels[i] = str(i)

        self.labels = labels
        self.anchura = anchura
        self.altura = niveles

        G1 = nx.DiGraph()
        G1.add_nodes_from(self.puntos)
        G1.add_edges_from(self.aristas)
        self.matriz = nx.adjacency_matrix(G1)
        traza.info('Salgo de la clase Topo')
        return


class Mapa(object):
    '''
    Esta clase modela mapas de puntos. El método num_cruces devuelve el número de curces del Mapa. Para crear
    un mapa hay que pasarle (pos, aristas).

    '''

    def __init__(self, pos, aristas):
        traza.info('Entro en la clase Mapa')
        self.pos = pos
        self.sop = {}
        self.aristas = aristas
        for key in pos:
            # x = pos[key][0]
            y = pos[key][1]
            if y not in self.sop:
                self.sop[y] = [key]
            else:
                self.sop[y].append(key)

        num_intervalos = max([k for k in self.sop])
        self.num_intervalos = num_intervalos
        self.niveles = range(num_intervalos + 1)
        traza.info('Salgo de la clase Mapa')

        return

    def num_cruces(self):

        cruces = 0
        registro_de_intersecciones = []
        for intervalo in range(1, self.num_intervalos + 1):
            for punto_bajo1 in self.sop[intervalo - 1]:
                for punto_bajo2 in self.sop[intervalo - 1]:
                    if punto_bajo1 <> punto_bajo2:
                        for punto_alto1 in self.sop[intervalo]:
                            for punto_alto2 in self.sop[intervalo]:
                                if punto_alto1 <> punto_alto2:
                                    cortan, arista1, arista2 = hay_corte(punto_bajo1, punto_bajo2, punto_alto1,
                                                                         punto_alto2, self.aristas, self.pos)
                                    if cortan:

                                        if ([arista1, arista2] not in registro_de_intersecciones) and (
                                                    [arista2, arista1] not in registro_de_intersecciones):
                                            registro_de_intersecciones.append([arista1, arista2])
                                            cruces = cruces + 1

        return cruces

    '''
    def num_verticales(self):
        num_verticales = 0
        for arista in self.aristas:
            if self.pos[arista[0]][0] == self.pos[arista[1]][0]:
                num_verticales = num_verticales + 1
        return num_verticales
    '''

    def factor_de_simetria(self):
        factor_de_simetria = 0
        for arista in self.aristas:
            if self.pos[arista[0]][0] == self.pos[arista[1]][0]:
                factor_de_simetria = factor_de_simetria + 12
            else:
                pendiente = (self.pos[arista[1]][1] - self.pos[arista[0]][1]) / (self.pos[arista[1]][0] - self.pos[
                    arista[0]][0])
                if abs(pendiente) == 1:
                    factor_de_simetria = factor_de_simetria + 4

        return factor_de_simetria


def optimo(mapa_inicial):
    """
    optimo es una fución que coge un mapa y devuelve un mapa isomorfo con el mínimo número de cortes.
    Para ello permutamos las posiciones de los puntos  hasta encontrar una permutación con menos cruces y
    devolvemos dicho mapa
    """

    # pos y sop no tienen la misma información. pos nos da las posiciones de cada punto
    # mientras que sop nos dice qué puntos están en cada uno de los niveles
    # Tenemos que permutar los puntos sobre las posiciones pos.
    # Por tanto tendremos que permutar las claves del diccionario pos dejando intactos sus valores
    # Primero hallarems las permutaciones válidas, es decir, aquellas que cambian los puntos pero
    # siempre limitando la permutación a cada uno de los niveles. Los puntos no pueden cambiar de nivel.

    posibles = []

    for nivel in mapa_inicial.niveles:
        tmp = {}
        tmp[nivel] = []
        for i in itertools.permutations(mapa_inicial.sop[nivel]):
            tmp[nivel].append(list(i))
        posibles.append(tmp)

    posibles2 = {}
    for i in mapa_inicial.niveles:
        posibles2[i] = posibles[i][i]

    ejecutable = '[['
    n_niveles = len(mapa_inicial.niveles)

    for i in range(n_niveles):
        ejecutable = ejecutable + 'x' + str(i) + ', '
    ejecutable2 = ejecutable[:-2] + ']'

    for i in range(n_niveles):
        ejecutable2 = ejecutable2 + ' for x' + str(i) + ' in posibles2[' + str(i) + ']'
    ejecutable2 = ejecutable2 + ']'

    ejecutable3 = 'despliegue = ' + ejecutable2

    exec (ejecutable3)

    # despliegue contiene las permutaciones que
    # hay que construir mapas para cada una de las permutaciones
    # y calcular su número de cruces
    # Hay que aplicar a pos cada una de las permutacones para encontrar el nuevo pos
    # Para ello hay hacer un biyección entre mapa_inicial.sop y cada uno de las permutaciones de despliegue
    # input()

    mapa_optimo = mapa_inicial
    numero_de_cruces = mapa_optimo.num_cruces()
    for k1 in despliegue:

        pos_permutado = permutamos(sop=mapa_inicial.sop, pos=mapa_inicial.pos, permutacion=k1)
        mapa_temporal = Mapa(pos_permutado, mapa_inicial.aristas)
        if mapa_temporal.num_cruces() < numero_de_cruces:
            mapa_optimo = mapa_temporal



    # Vamos a ver cuál tiene más simetría, es decir, menor factor de simetría, entre las configuraciones con menor
    # número de cruces

    num_cruces = mapa_optimo.num_cruces()
    factor_de_simetria = 0
    mapa_optimo2 = mapa_optimo
    for k1 in despliegue:

        pos_permutado = permutamos(sop=mapa_inicial.sop, pos=mapa_inicial.pos, permutacion=k1)
        mapa_temporal = Mapa(pos_permutado, mapa_inicial.aristas)
        if mapa_temporal.num_cruces() == num_cruces:
            if mapa_temporal.factor_de_simetria() > mapa_optimo2.factor_de_simetria():
                mapa_optimo2 = mapa_temporal
    return mapa_optimo2


def permutamos(sop, pos, permutacion):
    """
    Esta función lo que hace es generar un pos nuevo en función del pos viejo y de la permutación que se le pasa
    Devuelve un nuevo pos.
    """

    biyeccion = {}

    """
    Qué tenemos que hacer:
    1. Leer un punto
    2. Ver qué posición ocupa en sop. Sea fila , columna su posición
    3. Leer que punto de permutación está en la posición fila, columna

    """
    sop_matrix = []
    for nivel in sop:
        sop_matrix.append(sop[nivel])

    permutacion_matrix = permutacion

    biyeccion = {}
    x_sop = {}
    y_sop = {}

    for fila in range(len(sop_matrix)):
        for columna in range(len(sop_matrix[fila])):
            punto = sop_matrix[fila][columna]
            biyeccion[punto] = permutacion_matrix[fila][columna]


    # Construimos el nuevo pos con la biyección obtenida

    nuevo_pos = {}
    for punto in pos:
        nuevo_pos[biyeccion[punto]] = pos[punto]

    return nuevo_pos


def hay_corte(pb1, pb2, pa1, pa2, aristas, pos):
    pues_cortan = False
    aristas_que_intervienen = []
    a1 = 0
    a2 = 0

    if [pb1, pa1] in aristas:
        aristas_que_intervienen.append([pb1, pa1])
    if [pb1, pa2] in aristas:
        aristas_que_intervienen.append([pb1, pa2])
    if [pb2, pa1] in aristas:
        aristas_que_intervienen.append([pb2, pa1])
    if [pb2, pa2] in aristas:
        aristas_que_intervienen.append([pb2, pa2])

    for arista1 in aristas_que_intervienen:
        for arista2 in aristas_que_intervienen:
            x1 = float(pos[arista1[0]][0])
            y1 = float(pos[arista1[0]][1])
            x2 = float(pos[arista1[1]][0])
            y2 = float(pos[arista1[1]][1])
            x3 = float(pos[arista2[0]][0])
            y3 = float(pos[arista2[0]][1])
            x4 = float(pos[arista2[1]][0])
            y4 = float(pos[arista2[1]][1])
            cortan = True
            if arista1 == arista2:
                cortan = False
            if x1 == x3:
                cortan = False
            if x2 == x4:
                cortan = False
            if cortan == True:
                # Ahora vemos si hay corte



                if determinante((x1, y1), (x3, y3), (x4, y4)) > 0 and determinante((x2, y2), (x3, y3), (x4, y4)) > 0:
                    cortan = False
                if determinante((x1, y1), (x3, y3), (x4, y4)) < 0 and determinante((x2, y2), (x3, y3), (x4, y4)) < 0:
                    cortan = False

            if cortan:
                pues_cortan = True
                a1 = arista1
                a2 = arista2
    return pues_cortan, a1, a2


def determinante((a1, b1), (a2, b2), (a3, b3)):
    determinante = a2 * b3 - b2 * a3 - a1 * b3 + a3 * b1 + a1 * b2 - a2 * b1

    return determinante


def graph(topo):
    """
    Devuelve un grafo de NetworkX de la topología topo

    """
    resultado = nx.DiGraph()
    resultado.add_nodes_from(topo.puntos)
    resultado.add_edges_from(topo.aristas)
    return resultado


def powersetgen(seq):
    """
    Returns all the subsets of this set. This is a generator.

    """

    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powersetgen(seq[1:]):
            yield [seq[0]] + item

            yield item


def intersec(lista):
    """
    Halla la intersección de una colección de conjuntos
    lista es una lista cuyos elementos son listas. Devuelve una lista

    """
    if lista <> []:

        lista_frozen = set(frozenset(i) for i in lista)
        resultado = list(lista_frozen)[0]
        for i in lista_frozen:
            resultado = resultado & i
        resultado = list(resultado)
    else:
        resultado = []
    return resultado


def esta_lista1_dentro_de_lista2(lista1, lista2):
    """
    Utilidad para saber si una lista contiene a otra

    """
    resultado = False
    tamano1 = len(lista1)
    tamano2 = len(lista2)
    for i in range(0, tamano2 - tamano1 + 1):
        rebanada = lista2[i:i + tamano1]
        if lista1 == rebanada:
            resultado = True
    return resultado


def descendencia(G1, root, estructura, nivel):
    """
    Función recursiva que se utiliza para descubrir descendientes de un nodo en un poset

    """
    descendientes = G1.predecessors(root)
    if descendientes == []:
        hemos_terminado = True
    else:
        estructura.append([nivel - 1, descendientes])
        lo_ultimo_que_meto = [nivel - 1, descendientes]
        nivel = nivel - 1
        padre = root
        for hijo in descendientes:
            if not (nx.has_path(G1, padre, hijo) and nx.has_path(G1, hijo, padre)):
                root = hijo
                descendencia(G1, root, estructura, nivel)
            else:
                if lo_ultimo_que_meto in estructura:
                    estructura.remove(lo_ultimo_que_meto)
                    #estructura.append('Atencion, aqui hay ciclos')
    return estructura


def es_espacio_topologico(puntos, abiertos):
    """
    Comprueba si es un espacio topológico

    """
    es_espacio_topo = True
    if [] not in abiertos:
        es_espacio_topo = False
    if puntos not in abiertos:
        es_espacio_topo = False

    abiertos_frozenset = set(frozenset(i) for i in abiertos)
    # La unión está?
    for i in abiertos:
        for j in abiertos:
            union = set(i) | set(j)
            if not union in abiertos_frozenset:
                es_espacio_topo = False
    # La intersección está?
    for i in abiertos:
        for j in abiertos:
            interseccion = set(i) & set(j)
            if not interseccion in abiertos_frozenset:
                es_espacio_topo = False
    return es_espacio_topo


def es_t0(puntos, abiertos):
    """
    Comprueba si topo es T0?

    """
    resultado = True
    for i in puntos:
        for j in puntos:
            if i <> j:
                # Hay algún abierto tal que contenga a i pero no a j?
                distingue = False
                for abierto in abiertos:
                    if i in abierto:
                        if j not in abierto:
                            distingue = True
                    if j in abierto:
                        if i not in abierto:
                            distingue = True

                if distingue == False:
                    resultado = False
    return resultado


def todas(num_elementos):
    """
    Halla todas las topologías T0 con un número de elementos dado no isomorfas
    Devuelve una lista de topologías, no necesariamente no-isomorfas.
    """
    base = Set(range(1, num_elementos + 1))
    todas = []
    contador = 0
    for abiertos in powersetgen(base.powerset().theElements):
        if es_espacio_topologico(base.theElements, abiertos):
            basetopo = Topo(base.theElements, abiertos)
            if es_t0(basetopo):
                contador += 1
                # hasse_simple(basetopo)
                todas.append(basetopo)

    lista_de_topos = todas
    lista_de_no_isomorfas = []
    for t1 in lista_de_topos:
        no_esta_repetida = True
        for t2 in lista_de_no_isomorfas:
            DiGM = nx.isomorphism.DiGraphMatcher(graph(t1), graph(t2))

            if DiGM.is_isomorphic():
                no_esta_repetida = False
        if no_esta_repetida:
            lista_de_no_isomorfas.append(t1)
    return lista_de_no_isomorfas


def union_multi(conjuntos):
    """
    Se le da una lista de listas, conjunto de subconjuntos y devuelve el conjunto de todas las uniones
    Sirve para pasar de una base mínima a los abiertos de una topología

    """

    resultado = []

    for i in powersetgen(conjuntos):

        merged = list(itertools.chain.from_iterable(i))
        merged2 = list(set(merged))
        if merged2 not in resultado:
            resultado.append(merged2)
    i = resultado.index([])
    del resultado[i]

    return resultado


def de_base_a_topo(puntos, base):
    """
    Pasa de una base mínima a la topología correspondiente

    """

    abiertos = union_multi(base)
    abiertos.append([])

    topo = Topo(puntos, abiertos)

    return topo


def es_base(puntos, base):
    '''
    Si puntos o base no son listas, lo paso a listas
    puntos es una lista de puntos o una string de llaves
    base es una lista de listas de puntos o una string de llaves
    (i) Every pint in X is contained in a basis element
    (ii) Every point in the intersection of two basis elements is contained in a basis element contained in that
    intersection
    Adams, Franzosa pag. 29
    '''
    if isinstance(puntos, str):
        puntos = de_llaves_a_lista(de_corchetes_a_llaves(puntos))
    if isinstance(base, str):
        base = de_llaves_a_lista(de_corchetes_a_llaves(base))
    # Vamos con (i)


    resultado = True
    union = set([])
    for subconjunto in base:
        union = union.union(set(subconjunto))
    if union <> set(puntos):
        resultado = False
    if resultado == True:
        # Vamos con (ii)
        for sub1 in base:
            for sub2 in base:
                if sub1 <> sub2:
                    interseccion = list(set(sub1).intersection(sub2))
                    cumple_ii = True
                    for x in interseccion:
                        esta = False
                        for sub3 in base:
                            if x in sub3:
                                if set(sub3).issubset(set(interseccion)):
                                    esta = True
                        if esta == False:
                            cumple_ii = False
        if cumple_ii == False:
            resultado = False

    return resultado


def de_corchetes_a_llaves(ristra):
    resultado = ristra.replace('[', '{')
    resultado = resultado.replace(']', '}')
    return resultado


def de_llaves_a_corchetes(ristra):
    resultado = ristra.replace('{', '[')
    resultado = resultado.replace('}', ']')
    return resultado


def de_llaves_a_lista(ristra):
    resultado = ristra.replace('{', '[')
    resultado = resultado.replace('}', ']')
    exec ('result = ' + resultado)
    return result


def de_lista_a_llaves(lista):
    return str(lista)


def tiene_pinta_de_puntos(puntos):
    resultado = True
    # Solo puede tener espacios, corchetes, llaves, números y comas
    for x in puntos:
        if x not in [' ','[',']','{','}',',','0','1','2','3','4','5','6','7','8','9',]:
            resultado = False
    return resultado

def tiene_pinta_de_base(base):
    resultado = True
    # Solo puede tener espacios, corchetes, llaves, números y comas
    for x in base:
        if x not in [' ','[',']','{','}',',','0','1','2','3','4','5','6','7','8','9',]:
            resultado = False
    return resultado








# Pruebas
if __name__ == '__main__':
    puntos = [1, 2, 3, 4, 5, 6, 7]
    base = [[1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7], [3, 5, 6], [4, 6, 7], [5], [6], [7]]
    topologia = de_base_a_topo(puntos, base)
    # topologia.hasse2()


    # Matrices
    print
    print 'matriz = '
    print topologia.matriz
    print
    print 'The End'


