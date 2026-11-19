from pylab import *
import networkx as nx

# Parametros de la red
N = 100
k = 4
repeticiones = 30

valores_p = arange(0, 1.1, 0.1)


def initialize():
    global grados_promedio, agrupamientos, indice

    grados_promedio = []
    agrupamientos = []
    indice = 0


def observe():
    global grados_promedio, agrupamientos

    clf()

    # Grafica del grado promedio
    subplot(1, 2, 1)
    plot(valores_p[:len(grados_promedio)],
         grados_promedio, 'o-')

    xlabel('Probabilidad de reconexion (p)')
    ylabel('Grado promedio')
    title('Grado promedio - Watts-Strogatz')
    grid()

    # Grafica del coeficiente de agrupamiento
    subplot(1, 2, 2)
    plot(valores_p[:len(agrupamientos)],
         agrupamientos, 'o-')

    xlabel('Probabilidad de reconexion (p)')
    ylabel('Coeficiente de agrupamiento')
    title('Agrupamiento - Watts-Strogatz')
    grid()

    pause(0.5)


def update():
    global indice, grados_promedio, agrupamientos

    p = valores_p[indice]

    grados = []
    coeficientes = []

    # Experimentos Monte Carlo
    for i in range(repeticiones):

        # Crear red Watts-Strogatz
        g = nx.watts_strogatz_graph(N, k, p)

        # Calcular grado promedio
        grado = mean([g.degree(n) for n in g.nodes()])
        grados.append(grado)

        # Calcular coeficiente de agrupamiento
        clustering = nx.average_clustering(g)
        coeficientes.append(clustering)

    # Promedios de las simulaciones
    grados_promedio.append(mean(grados))
    agrupamientos.append(mean(coeficientes))

    print('p =', round(p, 1),
          '| Grado promedio =', round(grados_promedio[-1], 3),
          '| Agrupamiento =', round(agrupamientos[-1], 3))

    indice += 1


ioff()
initialize()

while indice < len(valores_p):
    update()
    observe()

print('Experimentos terminados')

show(block=True)