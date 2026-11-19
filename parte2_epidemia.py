from pylab import *
import networkx as nx
import builtins

# Parametros de la red
N = 100
k = 4
p_red = 0.1

# Parametros del modelo SIS adaptativo
p_i = 0.5
p_r = 0.2
p_s = 0.3


def initialize():
    global g, infectados_hist, susceptibles_hist, pasos

    # Crear red Watts-Strogatz
    g = nx.watts_strogatz_graph(N, k, p_red)
    g.pos = nx.spring_layout(g)

    # Todos los nodos comienzan susceptibles
    for i in g.nodes:
        g.nodes[i]['state'] = 0

    # Infectar 5 nodos aleatoriamente
    infectados = choice(list(g.nodes), size=5, replace=False)

    for i in infectados:
        g.nodes[i]['state'] = 1

    # Inicializar historial
    infectados_hist = []
    susceptibles_hist = []
    pasos = 0

    # Registrar estado inicial
    I = builtins.sum(g.nodes[n]['state'] for n in g.nodes)
    S = N - I

    infectados_hist.append(I)
    susceptibles_hist.append(S)


def observe():
    global g, infectados_hist, susceptibles_hist, pasos

    clf()

    # Calcular infectados y susceptibles
    I = builtins.sum(g.nodes[n]['state'] for n in g.nodes)
    S = N - I
    E = g.number_of_edges()

    # Grafica de la red
    subplot(1, 2, 1)

    nx.draw(
        g,
        cmap=cm.Wistia,
        vmin=0,
        vmax=1,
        node_color=[g.nodes[i]['state'] for i in g.nodes],
        pos=g.pos,
        with_labels=True
    )

    title('Modelo SIS adaptativo')

    # Grafica de infectados y susceptibles
    subplot(1, 2, 2)

    plot(infectados_hist, label='Infectados')
    plot(susceptibles_hist, label='Susceptibles')

    xlabel('Paso')
    ylabel('Numero de nodos')
    title('Evolucion de la epidemia')
    legend()
    grid()

    # Informacion de la simulacion
    suptitle(
        'Paso: ' + str(pasos) +
        ' | Infectados: ' + str(I) +
        ' | Susceptibles: ' + str(S) +
        ' | Enlaces: ' + str(E) +
        ' | Infeccion: ' + str(round(I/N*100, 1)) + '%'
    )

    tight_layout()

    pause(0.1)


def update():
    global g, infectados_hist, susceptibles_hist, pasos

    # Elegir un nodo aleatorio
    a = choice(list(g.nodes))

    if g.nodes[a]['state'] == 0:

        # Si el nodo es susceptible
        if g.degree(a) > 0:

            # Elegir un vecino aleatorio
            b = choice(list(g.neighbors(a)))

            # Si el vecino esta infectado
            if g.nodes[b]['state'] == 1:

                # Posibilidad de cortar el enlace
                if random() < p_s:
                    g.remove_edge(a, b)

                # Posibilidad de contagio
                else:
                    g.nodes[a]['state'] = (
                        1 if random() < p_i else 0
                    )

    else:

        # Si el nodo esta infectado,
        # puede recuperarse
        g.nodes[a]['state'] = (
            0 if random() < p_r else 1
        )

    # Calcular estados despues de la actualizacion
    I = builtins.sum(g.nodes[n]['state'] for n in g.nodes)
    S = N - I

    # Guardar datos
    infectados_hist.append(I)
    susceptibles_hist.append(S)

    pasos += 1


# Ejecutar simulacion
initialize()

ion()

while True:

    observe()

    # Verificar si la epidemia se extinguio
    I = builtins.sum(g.nodes[n]['state'] for n in g.nodes)

    if I == 0:
        print("La epidemia se ha extinguido.")
        print("Todos los nodos estan susceptibles.")
        print("Pasos de simulacion:", pasos)
        break

    update()

# Mostrar grafica final y mantener ventana abierta
show(block=True)