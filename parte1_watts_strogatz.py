from pylab import *
import networkx as nx


# Parametros de la red
N = 100
k = 4
repeticiones = 30


valores_p = arange(0, 1.1, 0.1)
grados_promedio = []


# Experimentos Monte Carlo
for p in valores_p:


    grados = []


    for i in range(repeticiones):


        g = nx.watts_strogatz_graph(N, k, p)


        grado = mean([g.degree(n) for n in g.nodes()])
        grados.append(grado)


    grados_promedio.append(mean(grados))


# Grafica
figure()


plot(valores_p, grados_promedio, 'o-')


xlabel('Probabilidad de reconexion (p)')
ylabel('Grado promedio')
title('Red Watts-Strogatz')
grid()


show()