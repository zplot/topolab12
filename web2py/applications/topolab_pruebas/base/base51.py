#!/usr/bin/python
# -*- coding: utf-8 -*-
#import collections
#import sys

import itertools

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

# **************************************************************







# Modela conjuntos
class Set(object):
    # El conjunto sólo debe crearse si está bien formado
    def __init__(self, conjunto):
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
    Esta clase modela espacios topológicos. Tiene puntos, abiertos, aristas y abiertos mínimos.

    '''

    def __init__(self, puntos, abiertos):
        # Hay que comprobar si realmente es un espacio topológico
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
        return

    def hasse2(self):
        """
        Vamos a pintar el diagrama de Hasse con el criterio de Eric Wofsey. Es decir, calculando los
        elementos mínimos y asignarles un rank = 0. Después subimos. Ver el doc.

        """
        print '--- Entro en Topo.hasse2'
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
        print 'elementos_minimos = ', elementos_minimos
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
        print 'niveles = ', niveles

        # Vamos a asignar rank a cada punto
        rank = {}
        sin_asignar_rank = G1.nodes()
        sin_asignar_rank_aux = G1.nodes()
        for x in elementos_minimos:
            rank[x] = 0
            sin_asignar_rank.remove(x)
            sin_asignar_rank_aux.remove(x)
        print 'sin_asignar_rank = ', sin_asignar_rank
        print 'sin_asignar_rank_aux = ', sin_asignar_rank_aux
        hemos_acabado = False
        if sin_asignar_rank_aux == []:
            hemos_acabado = True
        while not hemos_acabado:
            for x in sin_asignar_rank:
                y_menor_que_x = []
                for y in G1.nodes():
                    if x <> y:
                        if nx.has_path(G1, source=y, target=x):
                            y_menor_que_x.append(y)
                rango_de_los_ys = []
                for y in y_menor_que_x:
                    if y in rank:
                        rango_de_los_ys.append(rank[y]+1)
                rank[x] = max(rango_de_los_ys)
                sin_asignar_rank_aux.remove(x)
                if sin_asignar_rank_aux == []:
                    hemos_acabado = True
        print 'rank = ', rank
        print
        print

        # Ahora pasamos del diccionario rank al diccionario nivel, donde para cada nivel
        # tenemos los puntos que están en él.

        nivel = {}
        for i in range(0,niveles):
            nivel[i] = []
        for key in rank:
            a = rank[key]
            b = key
            nivel[a].append(b)
        print 'nivel = ', nivel
        # anchura del diagrama de hasse
        anchura = 0
        for i in nivel:
            if len(nivel[i]) > anchura:
                anchura = len(nivel[i])
        print 'anchura = ', anchura

        pos = {}
        for key in nivel:
            ancho_del_nivel = len(nivel[key])
            blancos_izda = (anchura - ancho_del_nivel)//2
            x_anterior = blancos_izda
            for punto in nivel[key]:
                x = x_anterior + 1
                x_anterior = x
                pos[punto] = (x, key)
        print 'pos = ', pos
        mapa1 = Mapa(pos, self.aristas)
        mapa2 = optimo(mapa1)

        # cogemos las posiciones del mapa óptimo
        pos = mapa2.pos



        # Ahora le ponemos etiquetas de los nodos
        labels = {}
        for i in self.puntos:
            labels[i] = str(i)



        # Pintamos el diagrama de Hasse

        nx.draw_networkx_nodes(G1, pos, node_size=200, nodelist=G1.nodes(), node_color='r')
        nx.draw_networkx_edges(G1, pos, alpha=0.5, width=1, arrows=False)
        nx.draw_networkx_labels(G1, pos, labels, font_size=9)
        plt.axis('off')
        plt.show()  # display
        return



class Mapa(object):
    '''
    Esta clase modela mapas de puntos. El método num_cruces devuelve el número de curces del Mapa. Para crear
    un mapa hay que pasarle (pos, aristas).

    '''
    def __init__(self, pos, aristas):
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
        print 'pos = ', self.pos
        print 'sop = ', self.sop
        num_intervalos = max([k for k in self.sop])
        self.num_intervalos = num_intervalos
        self.niveles = range(num_intervalos + 1)
        print 'num_intervalos = ', num_intervalos
        return

    def num_cruces(self):
        print '--- Entro en Mapa.num_cruces'
        cruces = 0
        registro_de_intersecciones = []
        for intervalo in range(1, self.num_intervalos+1):
            for punto_bajo1 in self.sop[intervalo -1]:
                for punto_bajo2 in self.sop[intervalo -1]:
                    if punto_bajo1 <> punto_bajo2:
                        for punto_alto1 in self.sop[intervalo]:
                            for punto_alto2 in self.sop[intervalo]:
                                if punto_alto1 <> punto_alto2:
                                    cortan, arista1, arista2 = hay_corte(punto_bajo1, punto_bajo2, punto_alto1, punto_alto2, self.aristas, self.pos)
                                    if cortan:
                                        print 40*'*'
                                        print 'cortan las aristas: ', arista1, arista2
                                        if ([arista1, arista2] not in registro_de_intersecciones) and ([arista2, arista1] not in registro_de_intersecciones):
                                            registro_de_intersecciones.append([arista1, arista2])
                                            cruces = cruces + 1
                                            print 'registro_de_intersecciones tmp = ', registro_de_intersecciones
                                            # print 'cruces = ', cruces
        print 'registro_de_intersecciones final = ', registro_de_intersecciones
        print 'num_cruces = ', cruces
        return cruces

    def num_verticales(self):
        num_verticales = 0
        for arista in self.aristas:
            if self.pos[arista[0]][0] == self.pos[arista[1]][0]:
                num_verticales = num_verticales + 1
        return num_verticales






def optimo(mapa_inicial):
    print '--- Entro en optimo'
    """
    optimo es una fución que coge un mapa y devuelve un mapa isomorfo con el mínimo número de cortes.
    Para ello permutamos las posiciones de los puntos  hasta encontrar una permutación con menos cruces y
    devolvemos dicho mapa
    """
    print
    print
    print
    print '-------------- Entramos en optimo --------------------------'
    print
    print 'mapa_inicial.pos = ', mapa_inicial.pos
    print 'mapa_inicial.sop = ', mapa_inicial.sop
    print

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

    print 'posibles = ', posibles
    posibles2 = {}
    for i in mapa_inicial.niveles:
        posibles2[i] = posibles[i][i]
    print 'posibles2 = ', posibles2





    print 'mapa_inicial.niveles = ', mapa_inicial.niveles
    ejecutable = '[['
    n_niveles = len(mapa_inicial.niveles)
    print 'n_niveles = ', n_niveles
    for i in range(n_niveles):
         ejecutable = ejecutable + 'x' + str(i) + ', '
    ejecutable2 = ejecutable[:-2] + ']'
    print 'ejecutable2 = ', ejecutable2



    for i in range(n_niveles):
        ejecutable2 = ejecutable2 + ' for x' + str(i) + ' in posibles2['+ str(i)+']'
    ejecutable2 = ejecutable2 + ']'
    print 'ejecutable2 = ', ejecutable2
    ejecutable3 = 'despliegue = ' + ejecutable2
    print 'ejecutable3 = ', ejecutable3
    exec (ejecutable3)
    print 'despliegue = ', despliegue
    # despliegue contiene las permutaciones que
    # hay que construir mapas para cada una de las permutaciones
    # y calcular su número de cruces
    # Hay que aplicar a pos cada una de las permutacones para encontrar el nuevo pos
    # Para ello hay hacer un biyección entre mapa_inicial.sop y cada uno de las permutaciones de despliegue
    # input()

    mapa_optimo = mapa_inicial
    numero_de_cruces = mapa_optimo.num_cruces()
    for k1 in despliegue:
        print ' *************************************** ', k1, '**********************************************'
        pos_permutado = permutamos(sop = mapa_inicial.sop, pos = mapa_inicial.pos, permutacion = k1)
        mapa_temporal = Mapa(pos_permutado, mapa_inicial.aristas)
        if mapa_temporal.num_cruces() < numero_de_cruces:
            mapa_optimo = mapa_temporal

    print 'mapa_inicial.pos = ', mapa_inicial.pos
    print 'mapa_optimo.pos  = ', mapa_optimo.pos
    # input()
    # Vamos a ver cuál tiene más lineas verticales
    num_cruces = mapa_optimo.num_cruces()
    num_verticales = 0
    mapa_optimo2 = mapa_optimo
    for k1 in despliegue:
        print ' *************************************** ', k1, '**********************************************'
        pos_permutado = permutamos(sop = mapa_inicial.sop, pos = mapa_inicial.pos, permutacion = k1)
        mapa_temporal = Mapa(pos_permutado, mapa_inicial.aristas)
        if mapa_temporal.num_cruces() == num_cruces:
            if mapa_temporal.num_verticales() > mapa_optimo2.num_verticales():
                mapa_optimo2 = mapa_temporal
    return mapa_optimo2




def permutamos(sop, pos, permutacion):
    """
    Esta función lo que hace es generar un pos nuevo en función del pos viejo y de la permutación que se le pasa
    Devuelve un nuevo pos.
    """
    print '--- Entro en permutamos'
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


    print 'sop_matrix =         ', sop_matrix
    print 'permutacion_matrix = ', permutacion_matrix

    biyeccion = {}
    x_sop = {}
    y_sop = {}


    for fila in range(len(sop_matrix)):
        for columna in range(len(sop_matrix[fila])):
            punto = sop_matrix[fila][columna]
            biyeccion[punto] = permutacion_matrix[fila][columna]

    print 'biyección = ', biyeccion

    # Construimos el nuevo pos con la biyección obtenida

    nuevo_pos = {}
    for punto in pos:
        nuevo_pos[biyeccion[punto]] = pos[punto]

    print 'pos = ', pos
    print 'nuevo_pos', nuevo_pos





    print

    return nuevo_pos








def hay_corte(pb1, pb2, pa1, pa2, aristas, pos):
    print ' --- Entro en hay_corte'
    pues_cortan = False
    aristas_que_intervienen = []
    a1 = 0
    a2 = 0

    # print 'todas las aristas = ', aristas
    if [pb1, pa1] in aristas:
        aristas_que_intervienen.append([pb1, pa1])
    if [pb1, pa2] in aristas:
        aristas_que_intervienen.append([pb1, pa2])
    if [pb2, pa1] in aristas:
        aristas_que_intervienen.append([pb2, pa1])
    if [pb2, pa2] in aristas:
        aristas_que_intervienen.append([pb2, pa2])
    print 'aristas_que_intervienen =', aristas_que_intervienen
    print 'pb1 = ', pb1
    print 'pb2 = ', pb2
    print 'pa1 = ', pa1
    print 'pa2 = ', pa2
    print
    print
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
                print 'vamos a ver si cortan', arista1, ' y ', arista2


                if determinante((x1,y1),(x3,y3),(x4,y4)) > 0 and determinante((x2,y2),(x3,y3),(x4,y4)) > 0:
                    cortan = False
                if determinante((x1,y1),(x3,y3),(x4,y4)) < 0 and determinante((x2,y2),(x3,y3),(x4,y4)) < 0:
                    cortan = False


            print 'las aristas ', arista1, ' y ', arista2, cortan, ' cortan'
            if cortan:
                pues_cortan = True
                a1 = arista1
                a2 = arista2
    return pues_cortan, a1, a2


def determinante((a1,b1),(a2,b2),(a3,b3)):
    # print '--- Entro en determinante'
    determinante = a2*b3 - b2*a3 - a1*b3 + a3*b1 + a1*b2 - a2*b1
    # print
    # print 'puntos = ', a1,b1,a2,b2,a3,b3
    # print 'determinante = ', determinante
    print
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
    resultado = []
    base = lista[0]
    for elemento in base:
        esta = True
        for conjunto in lista:
            if elemento not in conjunto:
                esta = False
        if esta:
            resultado.append(elemento)
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
    # La unión está?
    for i in abiertos:
        for j in abiertos:
            if list(set(i) | set(j)) not in abiertos:
                es_espacio_topo = False
    # La intersección está?
    for i in abiertos:
        for j in abiertos:
            if list(set(i) & set(j)) not in abiertos:
                es_espacio_topo = False
    return es_espacio_topo


def es_t0(topo):
    """
    Comprueba si topo es T0?

    """
    puntos = topo.puntos
    abiertos = topo.abiertos
    es_t0 = True
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
                    #print abiertos, ' no distingue ', i,' de ',j
                    es_t0 = False
    return es_t0


def hasse_simple(topo):
    """
    Dibuja un diagrama de Hasse simple sin colocación de puntos

    """
    G1 = nx.DiGraph()
    G1.add_nodes_from(topo.puntos)
    G1.add_edges_from(topo.aristas)
    nx.draw(G1)
    plt.axis('off')
    plt.show()
    return


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
                # print contador + 1, abiertos
                contador += 1
                # hasse_simple(basetopo)
                todas.append(basetopo)

    lista_de_topos = todas
    lista_de_no_isomorfas = []
    for t1 in lista_de_topos:
        no_esta_repetida = True
        for t2 in lista_de_no_isomorfas:
            DiGM = nx.isomorphism.DiGraphMatcher(graph(t1), graph(t2))
            # print ' Son isomorfos = ', DiGM.is_isomorphic()
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


def de_base_minima_a_topo(puntos, base_minima):
    """
    Pasa de una base mínima a la topología correspondiente

    """
    abiertos = union_multi(base_minima)
    abiertos.append([])
    topo = Topo(puntos, abiertos)
    return topo


def main():
    """
    Main. Flujo por defecto del programa

    """

    lista_de_topos = todas(4)
    print 'Número de topologías T0 no isomorfas = ', len(lista_de_topos)
    for topo in lista_de_topos:
        print
        print 'Abiertos = ', topo.abiertos
        print 'Mx = ', topo.Mx
        print 'Aristas = ', topo.aristas
        print
        topo.hasse2()

    puntos = [1,2,3,4,5,6]
    base_min = [[6, 2, 1], [5, 2, 1, 3], [4, 1], [3, 1], [2, 1]]
    topologia = de_base_minima_a_topo(puntos,base_min)
    print 'de_base_minima_a_topo puntos = ', topologia.puntos
    print 'de_base_minima_a_topo abiertos = ', topologia.abiertos
    print 'de_base_minima_a_topo aristas = ', topologia.aristas
    print 'Mx = ', topologia.Mx
    topologia.hasse2()


    # puntos = [1,2,3,4]
    # abiertos = [[1, 2, 3, 4], [1, 2, 3], [1, 2], [1], []]
    # topologia = Topo(puntos, abiertos)
    # print 'puntos = ', topologia.puntos
    # print 'abiertos = ', topologia.abiertos
    # print 'aristas = ', topologia.aristas
    # print 'Mx = ', topologia.Mx
    # topologia.hasse2()
    # return



# Aquí empieza a ejecutarse el programa. Probamos las cosas
main()



