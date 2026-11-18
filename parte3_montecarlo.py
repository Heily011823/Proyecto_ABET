from pylab import *
import networkx as nx
import builtins

# Parametros de la red
N = 100
k = 4
p_red = 0.1


# Parametros de la epidemia
p_i = 0.5
p_r = 0.2


valores_ps = arange(0, 1.1, 0.1)


simulaciones = 30
pasos = 300




def initialize():
    global g


    g = nx.watts_strogatz_graph(N, k, p_red)


    for i in g.nodes:
        g.nodes[i]['state'] = 0


    infectados = choice(list(g.nodes), size=5, replace=False)


    for i in infectados:
        g.nodes[i]['state'] = 1




def update(ps):
    global g


    a = choice(list(g.nodes))


    if g.nodes[a]['state'] == 0:


        if g.degree(a) > 0:


            b = choice(list(g.neighbors(a)))


            if g.nodes[b]['state'] == 1:


                if random() < ps:
                    g.remove_edge(a, b)


                else:
                    if random() < p_i:
                        g.nodes[a]['state'] = 1


    else:


        if random() < p_r:
            g.nodes[a]['state'] = 0




def simulation(ps):


    initialize()


    infectados = []
    enlaces = []


    for t in range(pasos):


        for i in range(N):
            update(ps)


        I = builtins.sum(g.nodes[n]['state'] for n in g.nodes)
        E = g.number_of_edges()


        infectados.append(I)
        enlaces.append(E)


    return infectados, enlaces




# Experimentos Monte Carlo


resultados_I = []
resultados_E = []


for ps in valores_ps:


    todas_I = []
    todas_E = []


    for i in range(simulaciones):


        I, E = simulation(ps)


        todas_I.append(I)
        todas_E.append(E)


    promedio_I = mean(array(todas_I), axis=0)
    promedio_E = mean(array(todas_E), axis=0)


    resultados_I.append(promedio_I)
    resultados_E.append(promedio_E)


    # Clasificacion de la epidemia
    extinciones = builtins.sum(1 for serie in todas_I if serie[-1] == 0)

    porcentaje = extinciones / simulaciones


    nivel_final = mean(promedio_I[int(pasos * 0.8):])


    if porcentaje >= 0.9:
        estado = 'Erradicada'


    elif nivel_final >= N * 0.5:
        estado = 'Creciente'


    else:
        estado = 'Sostenida'


    print('p_s =', round(ps, 1),
          '| Extincion =', round(porcentaje * 100, 1), '%',
          '| Estado =', estado)




# Grafica de infectados


figure()


for i in range(len(valores_ps)):
    plot(resultados_I[i],
         label='p_s = ' + str(round(valores_ps[i], 1)))


xlabel('Tiempo')
ylabel('Numero de infectados')
title('Promedio de infectados - Monte Carlo')
legend()
grid()
show()




# Grafica de enlaces


figure()


for i in range(len(valores_ps)):
    plot(resultados_E[i],
         label='p_s = ' + str(round(valores_ps[i], 1)))


xlabel('Tiempo')
ylabel('Numero de enlaces')
title('Promedio de enlaces - Monte Carlo')
legend()
grid()
show()



