import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import os
import networkx as nx
import random
import math
import time
from copy import copy


def random_point(r1, r2, bb, name):
    x = random.randrange(r1, r2)
    y = random.randrange(0, r2)
    for i in bb:
        if collisions(i, x, y):
            x, y = random_point(r1, r2, bb, name)
    if name == 'start' or name == 'goal' or name == 'q_rand':
        plt.text(x, y, name, fontsize=12)
    return x, y


def obs_collision(bboxes, bb):  # verifica che il nuovo ostacolo non interseca nessuno di quelli esistenti
    for b in bboxes:
        if (Bbox.intersection(b, bb)) is not None:
            return True
    return False


def generate_obstacles(boxes, ax, range):
    while len(boxes) < 5:

        a = random.randrange(10, range)
        b = random.randrange(0, range)
        obs = Rectangle((a, b), random.randint(1, 15), random.randint(1, 15), color='silver')

        if len(boxes) == 0:
            boxes.append(obs.get_bbox())
            new_obs = copy(obs)
            ax[0].add_patch(obs)
            ax[1].add_patch(new_obs)

        elif len(boxes) > 0 and not obs_collision(boxes, obs.get_bbox()):
            boxes.append(obs.get_bbox())
            new_obs = copy(obs)
            ax[0].add_patch(obs)
            ax[1].add_patch(new_obs)
        else:
            pass
    return boxes, ax


def collisions(bbox, x, y):
    collision = bbox.contains(x, y)  # se il pnt è nell'ostacolo
    return collision


def random_samples(n_samples, bb, r1, r2, graph, dict_nodes):  # non usata, genera randomicamente dei nodi
    for j in range(0, n_samples):
        q = random_point(r1, r2, bb, j)
        dict_nodes[j] = q
        graph.add_node(j, text=j)
    return graph, dict_nodes


def create_graph(graph, s, e):
    n = {'start': s, 'goal': e}  # nome nodo e coordinate del nodo
    graph.add_node('start', text='start')
    graph.add_node('goal', text='goal')
    return graph, n


def knn(graph_nodes, q_rand, n):
    neighbors = {}
    dist = {}
    d = 0
    if len((graph_nodes.keys())) >= n:
        for name, q in graph_nodes.items():
            if q != q_rand:
                dist[name] = math.dist(q_rand, q)  # calcola la dist e associa il nodo q

        while len(neighbors.keys()) != n - 1 and len(dist.values()) != 0:  # Find n neighbors
            tmp = min(dist.values())  # nodo a minor distanza da q_rand
            for k in dist:  # k = nome nodo vicino
                if dist[k] == tmp:
                    neighbors[k] = graph_nodes[k]
                    d = k
            del dist[d]
    return neighbors


def eps_n(graph_nodes, q_rand, eps):
    neighbors = {}
    for name, q in graph_nodes.items():
        if q != q_rand:
            dist = math.dist(q_rand, q)
            if dist < eps:  # trovare i neighbors entro il raggio eps
                neighbors[name] = q
    return neighbors


def free_path(q_rand, q, bboxes):  # q = q_near, intersezione con obs
    vertices = [q_rand, q]
    for i in bboxes:
        path = Path(vertices, codes=[1, 2])
        if path.intersects_bbox(i):
            return False
    return True


def node_color(g_nodes, path):
    c = []
    for node in g_nodes:
        if node in path:
            if node == 'start' or node == 'goal':
                c.append('red')
            elif node in path:
                c.append('blue')
        else:
            c.append('lightblue')
    return c


def prm(graph, dict_nodes, r1, r2, bboxes, alg, parameter, ax, n_iter, j, fig):  # alg = knn or eps_n
    edges = {}
    k = 0
    n_node = 50
    x = 1
    while len(graph.nodes) < n_node or (not nx.has_path(graph, 'start', 'goal')):
        q_rand = random_point(r1, r2, bboxes, str(k))  # se c'è collisione ricalcola
        dict_nodes[str(k)] = q_rand  # aggiunge q_rand al grafo
        graph.add_node(str(k), text=str(k))

        edges[str(k)] = q_rand

        if alg == 'eps_n':
            eps = parameter
            nbrs = eps_n(dict_nodes, q_rand, eps)  # cercare tutti i nodi vicini a q_rand
        elif alg == 'knn':
            n = parameter
            nbrs = knn(dict_nodes, q_rand, n)
        else:
            print('errore')
            break

        for name, q in nbrs.items():
            if free_path(q_rand, q, bboxes):
                graph.add_edge(str(k), name)  # aggiungere arco tra i q_near e q_rand
                edges[name] = q
        k += 1

        '''  per fare il plot delle figure per creare il video, commentando if j == n_iter-1
        if nx.has_path(graph, 'start', 'goal') and len(graph.nodes) >= n_node:
            shortest_path = nx.shortest_path(graph, 'start', 'goal')
            color_map = node_color(dict_nodes.keys(), shortest_path)
            color = ['red' if i in shortest_path and j in shortest_path else 'black' for (i, j) in graph.edges()]
        else:
            color_map = ['red' if i == 'start' or i == 'goal' else 'lightblue' for i in graph.nodes()]
            color = 'black'

        # nx.draw(graph, pos=dict_nodes, ax=ax, node_size=30, node_color=color_map, edge_color=color)
        nx.draw_networkx_nodes(graph, pos=dict_nodes, nodelist=list(dict_nodes.keys()),
                               node_color=color_map, node_size=30, ax=ax)
        nx.draw_networkx_edges(graph, pos=edges, edge_color=color, ax=ax, width=0.5)

        ax.set_title('PRM con ' + alg)
        ax.set(xlim=(-2, 75), ylim=(-2, 75))

        # plt.pause(0.001)

        # plt.savefig(alg + '_img_' + str(x) + '.png')
        # x += 1

        '''
    if j == n_iter-1:  # se è l'ultima prova, mostra i grafici
        shortest_path = nx.shortest_path(graph, 'start', 'goal')

        color_map = node_color(dict_nodes.keys(), shortest_path)
        nx.draw_networkx_nodes(graph, pos=dict_nodes, nodelist=list(dict_nodes.keys()),
                               node_color=color_map, node_size=30, ax=ax)

        color = ['red' if i in shortest_path and j in shortest_path else 'black' for (i, j) in graph.edges()]
        # disegnare in rosso gli archi che creano il cammino più corto
        nx.draw_networkx_edges(graph, pos=edges, edge_color=color, ax=ax)

        ax.set_title('PRM con ' + alg)

        print('\nInsieme dei nodi vicini calcolato con: ' + alg, '\nNumero nodi nel shortest_path: ',
              len(shortest_path),
              '\nNumero di componenti connesse: ', nx.number_connected_components(graph),
              '\nNumero nodi generati nel grafo', graph.order())


def main():
    r = 50  # range posizione
    r_start = 20
    r_goal = 70
    eps = 6
    n = 10
    n_iter = 5

    computation_times_eps_n = []
    computation_times_knn = []
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    c_obs = []
    c_obs, ax = generate_obstacles(c_obs, ax, r)

    start = random_point(0, r_start, c_obs, 'start')
    goal = random_point(r, r_goal, c_obs, 'goal')

    for i in range(n_iter):
        print(i)
        g = nx.Graph()  # To create an empty undirected graph

        g, nodes_g = create_graph(g, start, goal)  # creazione grafo con solo start e goal

        start_time = time.time()  # con eps piccolo impiega più tempo, es 2.075
        prm(g, nodes_g, 0, r_goal, c_obs, 'eps_n', eps, ax[0], n_iter, i, fig)
        end_time = time.time()
        computation_times_eps_n.append(end_time - start_time)

        g = nx.Graph()
        g, nodes_g = create_graph(g, start, goal)  # creazione grafo con solo start e goal

        start_time = time.time()  # con n piccolo più veloce ma pochi nodi nel grafo (quando il grafo è poco denso)
        prm(g, nodes_g, 0, r_goal, c_obs, 'knn', n, ax[1], n_iter, i, fig)
        end_time = time.time()
        computation_times_knn.append(end_time - start_time)

    print('\nNumero di prove = ', n_iter,
          '\ncomputation_times_eps_n medio = ', (sum(computation_times_eps_n)) / len(computation_times_eps_n),
          '\ncomputation_times_knn medio = ', (sum(computation_times_knn)) / len(computation_times_knn))

    plt.show()


if __name__ == '__main__':
    main()

    #os.system("ffmpeg -r 8 -i C:/Users/dicos/PycharmProjects/lab/eps_n_img_%d.png -vcodec mpeg4 -y prm_eps_n.mp4")
    #os.system("ffmpeg -r 8 -i C:/Users/dicos/PycharmProjects/lab/knn_img_%d.png -vcodec mpeg4 -y prm_knn.mp4")
