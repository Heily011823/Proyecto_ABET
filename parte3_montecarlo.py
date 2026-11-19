
from pylab import *
import networkx as nx
import builtins

# ==========================================
# PARAMETROS DE LA RED
# ==========================================

N = 100
k = 4
p_red = 0.1

# ==========================================
# PARAMETROS DE LA EPIDEMIA
# ==========================================

p_i = 0.5
p_r = 0.2

valores_ps = arange(0, 1.1, 0.1)

simulaciones = 30
pasos = 300


# ==========================================
# CREAR E INICIALIZAR LA RED
# ==========================================

def initialize():
    global g

    # Crear red Watts-Strogatz
    g = nx.watts_strogatz_graph(N, k, p_red)

    # Todos los nodos comienzan susceptibles
    for i in g.nodes:
        g.nodes[i]['state'] = 0

    # Seleccionar 5 nodos infectados aleatoriamente
    infectados = choice(list(g.nodes), size=5, replace=False)

    for i in infectados:
        g.nodes[i]['state'] = 1


# ==========================================
# ACTUALIZACION DEL MODELO SIS
# ==========================================

def update(ps):
    global g

    # Seleccionar un nodo aleatorio
    a = choice(list(g.nodes))

    if g.nodes[a]['state'] == 0:

        # Si el nodo es susceptible
        if g.degree(a) > 0:

            # Seleccionar uno de sus vecinos
            b = choice(list(g.neighbors(a)))

            # Si el vecino esta infectado
            if g.nodes[b]['state'] == 1:

                # Posibilidad de romper el enlace
                if random() < ps:
                    g.remove_edge(a, b)

                # Posibilidad de contagio
                else:
                    if random() < p_i:
                        g.nodes[a]['state'] = 1

    else:

        # Si esta infectado, puede recuperarse
        if random() < p_r:
            g.nodes[a]['state'] = 0


# ==========================================
# EJECUTAR UNA SIMULACION
# ==========================================

def simulation(ps):
    global g

    initialize()

    infectados = []
    enlaces = []

    for t in range(pasos):

        # Cada paso realiza 100 actualizaciones
        for i in range(N):
            update(ps)

        # Contar infectados
        I = builtins.sum(
            g.nodes[n]['state'] for n in g.nodes
        )

        # Contar enlaces
        E = g.number_of_edges()

        infectados.append(I)
        enlaces.append(E)

    return infectados, enlaces


# ==========================================
# GRAFICAR RESULTADOS
# ==========================================

def observe():
    global resultados_I, resultados_E

    clf()

    # Grafica de infectados promedio
    subplot(1, 2, 1)

    for i in range(len(resultados_I)):
        plot(
            resultados_I[i],
            label='p_s = ' + str(round(valores_ps[i], 1))
        )

    xlabel('Tiempo')
    ylabel('Numero de infectados')
    title('Promedio de infectados - Monte Carlo')
    legend()
    grid()

    # Grafica de enlaces promedio
    subplot(1, 2, 2)

    for i in range(len(resultados_E)):
        plot(
            resultados_E[i],
            label='p_s = ' + str(round(valores_ps[i], 1))
        )

    xlabel('Tiempo')
    ylabel('Numero de enlaces')
    title('Promedio de enlaces - Monte Carlo')
    legend()
    grid()

    tight_layout()
    pause(0.1)


# ==========================================
# EXPERIMENTOS MONTE CARLO
# ==========================================

resultados_I = []
resultados_E = []

# Guardar los resultados de la tabla
tabla_resultados = []

indice = 0

# Activar modo interactivo
ion()

while indice < len(valores_ps):

    ps = valores_ps[indice]

    todas_I = []
    todas_E = []

    # Ejecutar 30 simulaciones independientes
    for i in range(simulaciones):

        I, E = simulation(ps)

        todas_I.append(I)
        todas_E.append(E)

    # Convertir los resultados en arreglos
    todas_I = array(todas_I)
    todas_E = array(todas_E)

    # ======================================
    # PROMEDIOS DE LAS SIMULACIONES
    # ======================================

    promedio_I = mean(todas_I, axis=0)
    promedio_E = mean(todas_E, axis=0)

    resultados_I.append(promedio_I)
    resultados_E.append(promedio_E)

    # ======================================
    # RESULTADOS FINALES
    # ======================================

    # Valores finales de cada simulacion
    infectados_finales = todas_I[:, -1]
    enlaces_finales = todas_E[:, -1]

    # Promedios finales
    I_final = mean(infectados_finales)
    E_final = mean(enlaces_finales)

    # Error estandar de los valores finales
    error_I = std(infectados_finales, ddof=1) / sqrt(simulaciones)
    error_E = std(enlaces_finales, ddof=1) / sqrt(simulaciones)

    # ======================================
    # CLASIFICACION DE LA EPIDEMIA
    # ======================================

    # Contar simulaciones que terminan sin infectados
    extinciones = builtins.sum(
        1 for serie in todas_I if serie[-1] == 0
    )

    porcentaje = (extinciones / simulaciones) * 100

    # Promedio de infectados durante el ultimo 20 %
    nivel_final = mean(
        promedio_I[int(pasos * 0.8):]
    )

    # Aplicar criterios de clasificacion
    if porcentaje >= 90:
        estado = 'Erradicada'

    elif nivel_final >= N * 0.5:
        estado = 'Creciente'

    else:
        estado = 'Sostenida'

    # ======================================
    # GUARDAR RESULTADOS
    # ======================================

    tabla_resultados.append([
        round(ps, 1),
        I_final,
        E_final,
        error_I,
        error_E,
        porcentaje,
        estado
    ])

    # Mostrar resultados de cada valor de ps
    print('\nProbabilidad de ruptura:', round(ps, 1))
    print('Infectados finales promedio:', round(I_final, 2))
    print('Enlaces finales promedio:', round(E_final, 2))
    print('Error estandar de infectados:', round(error_I, 3))
    print('Error estandar de enlaces:', round(error_E, 3))
    print('Extincion:', round(porcentaje, 1), '%')
    print('Estado:', estado)

    indice += 1

    # Actualizar graficas
    observe()


# ==========================================
# MOSTRAR TABLA FINAL
# ==========================================

print('\n')
print('=' * 105)
print('TABLA FINAL DE RESULTADOS - EXPERIMENTOS MONTE CARLO')
print('=' * 105)

print(
    f"{'p_s':<8}"
    f"{'I final':<13}"
    f"{'E final':<13}"
    f"{'Error I':<13}"
    f"{'Error E':<13}"
    f"{'Extincion':<15}"
    f"{'Clasificacion':<15}"
)

print('-' * 105)

for fila in tabla_resultados:

    ps, I, E, err_I, err_E, ext, estado = fila

    print(
        f"{ps:<8.1f}"
        f"{I:<13.2f}"
        f"{E:<13.2f}"
        f"{err_I:<13.3f}"
        f"{err_E:<13.3f}"
        f"{ext:<15.1f}"
        f"{estado:<15}"
    )

print('=' * 105)
print('Experimentos terminados.')

# Mantener las graficas abiertas
show(block=True)
