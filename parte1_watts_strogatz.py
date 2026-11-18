from pylab import *
import networkx as nx


# Parametros de la red
N = 100
k = 4
repeticiones = 30


valores_p = arange(0, 1.1, 0.1)


grados_promedio = []
agrupamientos = []


# Experimentos Monte Carlo
for p in valores_p:


    grados = []
    coeficientes = []


    for i in range(repeticiones):


        # Crear red Watts-Strogatz
        g = nx.watts_strogatz_graph(N, k, p)


        # Calcular grado promedio
        grado = mean([g.degree(n) for n in g.nodes()])
        grados.append(grado)


        # Calcular coeficiente de agrupamiento
        clustering = nx.average_clustering(g)
        coeficientes.append(clustering)


    # Promedios de las 30 simulaciones
    grados_promedio.append(mean(grados))
    agrupamientos.append(mean(coeficientes))




# Mostrar resultados
print('Resultados de Watts-Strogatz')
print('--------------------------------')


for i in range(len(valores_p)):


    print('p =', round(valores_p[i], 1),
          '| Grado promedio =', round(grados_promedio[i], 3),
          '| Agrupamiento =', round(agrupamientos[i], 3))




# Grafica del grado promedio
figure()


plot(valores_p, grados_promedio, 'o-')


xlabel('Probabilidad de reconexion (p)')
ylabel('Grado promedio')
title('Grado promedio - Watts-Strogatz')
grid()


show()




# Grafica del coeficiente de agrupamiento
figure()


plot(valores_p, agrupamientos, 'o-')


xlabel('Probabilidad de reconexion (p)')
ylabel('Coeficiente de agrupamiento')
title('Agrupamiento - Watts-Strogatz')
grid()


show()