# -*- coding: utf-8 -*-

# Simplified interface to matplotlib
# Authors: Massimo Di Pierro & Laurent Peuch
# License: 3-clause BSD (c) 2012

# Ficheros que dependen de este: matplotlib

from cStringIO import StringIO

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Ellipse
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.text import Text


class Canvas(object):

    def __init__(self, title='title', xlab='x', ylab='y', xrange=None, yrange=None):
        self.fig = Figure()
        self.fig.set_facecolor('white')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        # self.ax.set_xlabel(xlab)
        # self.ax.set_ylabel(ylab)
        self.ax.set_axis_off()
        self.ax.set_aspect('equal')
        if xrange:
            self.ax.set_xlim(xrange)
        if yrange:
            self.ax.set_ylim(yrange)
        self.legend = []

    def save(self, filename='plot.png'):
        if self.legend:
            legend = self.ax.legend([e[0] for e in self.legend],[e[1] for e in self.legend])
            legend.get_frame().set_alpha(0.7)
        if filename:
            FigureCanvasAgg(self.fig).print_png(open(filename, 'wb'))
        else:
            s = StringIO()
            FigureCanvasAgg(self.fig).print_png(s)
            return s.getvalue()

    def binary(self):
        return self.save(None)

    def hist(self, data, bins=20, color='blue', legend=None):
        q = self.ax.hist(data, bins)
        if legend:
            self.legend.append((q[0], legend))
        return self

    def plot(self, data, color='blue', style='-', width=2, legend=None):
        x, y = [p[0] for p in data], [p[1] for p in data]
        q = self.ax.plot(x, y, linestyle=style, linewidth=width, color=color)
        if legend:
            self.legend.append((q[0],legend))
        return self

    def errorbar(self, data, color='black', marker='o', width=2, legend=None):
        x,y,dy = [p[0] for p in data], [p[1] for p in data], [p[2] for p in data]
        q = self.ax.errorbar(x, y, yerr=dy, fmt=marker, linewidth=width, color=color)
        if legend:
            self.legend.append((q[0],legend))
        return self

    def ellipses(self, data, color='blue', width=0.01, height=0.01):
        for point in data:
            x, y = point[:2]
            dx = point[2] if len(point)>2 else width
            dy = point[3] if len(point)>3 else height
            ellipse = Ellipse(xy=(x, y), width=dx, height=dy)
            self.ax.add_artist(ellipse)
            ellipse.set_clip_box(self.ax.bbox)
            ellipse.set_alpha(0.5)
            ellipse.set_facecolor(color)
        return self

    def imshow(self, data, interpolation='bilinear'):
        self.ax.imshow(data).set_interpolation(interpolation)
        return self

    def hasse(self, topologia):

        puntos = topologia.puntos
        aristas = topologia.aristas
        labels = topologia.labels
        pos_optima = topologia.pos_optima
        anchura = topologia.anchura
        altura = topologia.altura

        # Parametros de dibujo
        # puntos
        color_del_punto = '#ff0000'
        radio_del_punto = 0.09
        alpha_del_punto = 1.
        # aristas
        color_de_la_arista = '#000000'
        alpha_de_la_arista = 1
        tipo_de_marker = 'o'
        tamano_del_marker = 15
        color_del_marker = '#90e630'
        color_del_borde_del_marker = '#000000'
        ancho_del_borde_del_marker = .6
        # textos
        shift_x = -.02
        shift_y = -.04
        tamano_texto = 10

        # Pintamos las aristas
        for arista in aristas:
            las_x = [(pos_optima[arista[0]][0], pos_optima[arista[1]][0])]
            las_y = [(pos_optima[arista[0]][1], pos_optima[arista[1]][1])]
            linea = Line2D(las_x, las_y, color=color_de_la_arista, alpha=alpha_de_la_arista, marker=tipo_de_marker, markerfacecolor=color_del_marker, markeredgecolor=color_del_borde_del_marker, markeredgewidth=ancho_del_borde_del_marker, markersize=tamano_del_marker )
            self.ax.add_artist(linea)


        '''
        # Pintamos los puntos. Funciona OK pero no lo usamos porque tenemos markers en las líneas
        for i in puntos:
            print pos_optima[i][0], pos_optima[i][1]
            circle = Circle(xy=(pos_optima[i][0], pos_optima[i][1]), radius=radio_del_punto, color=color_del_punto, alpha = alpha_del_punto)
            self.ax.add_artist(circle)
        '''

        # Pintamos los puntos sin conexión. Pintamos todos.
        for i in puntos:
            linea_suelta = Line2D([pos_optima[i][0],pos_optima[i][0]], [pos_optima[i][1],pos_optima[i][1]], color=color_de_la_arista, alpha=alpha_de_la_arista, marker=tipo_de_marker, markerfacecolor=color_del_marker, markeredgecolor=color_del_borde_del_marker, markeredgewidth=ancho_del_borde_del_marker, markersize=tamano_del_marker )
            self.ax.add_artist(linea_suelta)


        # Vamos con los nombres de los puntos
        for i in puntos:
            texto = Text(x=pos_optima[i][0]+shift_x, y=pos_optima[i][1]+shift_y, text=labels[i], fontsize=tamano_texto)
            self.ax.add_artist(texto)


        return self


