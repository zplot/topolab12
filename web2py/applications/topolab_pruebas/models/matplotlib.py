# coding: utf8






from mdipierro_canvas2 import *
from modulo_math import *












def my_hasse1(puntos, base):
    '''
    En esta función vamos a recibir los puntos y la base mínima y vamos a generar las posiciones
    de los puntos óptima del diagrama de Hasse y se lo pasaremos a Canvas para que los pinte
    '''

    logger.info('Entro en matplotlib -> my_hasse1')
    # Pasamos de strings a listas si es necesario
    if isinstance(puntos,str):
        puntos = de_llaves_a_lista(de_corchetes_a_llaves(puntos))
    if isinstance(base,str):
        base = de_llaves_a_lista(de_corchetes_a_llaves(base))
    topologia = de_base_a_topo(puntos,base)
    #factor_h = 1.290909. No lo usamos porque hemos puesto aspect = 'equal'
    factor_h = 1
    logger.info('Salgo de matplotlib -> my_hasse1')
    return Canvas('Hasse Diagram', xrange = (0,(topologia.anchura+1)*factor_h), yrange = (-1,topologia.altura)).hasse(topologia).binary()






