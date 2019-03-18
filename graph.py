import os
import random
from threading import Lock

import networkx as nx


class Graph:
    DIGRAPH_FILE = "digraph.gml"
    GRAPH_FILE = "graph.gml"

    def __init__(self, dir):
        self.dig_path = os.path.join(dir, self.DIGRAPH_FILE)
        self.g_path = os.path.join(dir, self.GRAPH_FILE)

        self.mutex = Lock()
        if os.path.isfile(self.g_path):
            print("Loading graph from %s %s" % (self.g_path, self.dig_path))
            self.g = nx.read_gml(self.g_path)
            self.dig = nx.read_gml(self.dig_path)
        else:
            print("Creating graph at %s %s" % (self.g_path, self.dig_path))
            self.g = nx.Graph()
            self.dig = nx.DiGraph()

    def __del__(self):
        # self.save()
        pass

    def add_ts(self, page, binding_pages):
        with self.mutex:
            self._add(page, binding_pages)

    def _add(self, page, binding_pages):
        edges = [(page, link) for link in binding_pages]
        self.g.add_edges_from(edges)
        self.dig.add_edges_from(edges)

    def save(self):
        with self.mutex:
            print("Saving graphs %s %s" % (self.dig_path, self.g_path))
            nx.write_gml(self.g, self.g_path)
            nx.write_gml(self.dig, self.dig_path)

    def add_max(self, deg, v, list_v: list):
        max_c = 100
        i = 0
        for pair in list_v:
            if deg > pair[0]:
                break
            i += 1
        list_v.insert(i, (deg, v))

        if len(list_v) > max_c:
            list_v.remove(list_v[-1])

    def delete_max(self, to_rm):
        rm_num = [1, 10, 100]
        i = 0
        for pair_v in to_rm:
            self.g.remove_node(pair_v[1])
            self.dig.remove_node(pair_v[1])
            i += 1
            if i in rm_num:
                print("Deleted:", i)
                # print("Mean len:", nx.average_shortest_path_length(self.dig))
                # print("Diameter:", nx.diameter(self.g))
                print("Clustering coefficient:", nx.average_clustering(self.g))

    def shortest_paths_con(self):
        print("Shortest paths")
        sh_paths = dict(nx.shortest_path_length(self.g))
        sh_paths_con = {}
        for v in sh_paths.values():
            for path in v.values():
                if path in sh_paths_con:
                    sh_paths_con[path] += 1
                else:
                    sh_paths_con[path] = 1

        for key, val in sh_paths_con.items():
            print(key, val)

    def analyze(self):
        in_deg_con = {}
        out_deg_con = {}
        to_remove = []
        max_in = []
        max_out = []

        for v in self.dig.nodes:
            out_deg = self.dig.out_degree(v)
            if out_deg in out_deg_con:
                out_deg_con[out_deg] += 1
            else:
                out_deg_con[out_deg] = 1
            self.add_max(out_deg, v, max_out)
        self.dig.remove_nodes_from(to_remove)
        self.g.remove_nodes_from(to_remove)

        for v in self.dig.nodes:
            in_deg = self.dig.in_degree(v)
            if in_deg in in_deg_con:
                in_deg_con[in_deg] += 1
            else:
                in_deg_con[in_deg] = 1
            self.add_max(in_deg, v, max_in)
        n = self.dig.number_of_nodes()
        print("All vertices: %s" % n)
        print("All edges: %d" % len(self.dig.edges))
        print("Mean deg: %d" % (len(self.dig.edges) / self.dig.number_of_nodes()))

        # print("In deg")
        # for key, val in in_deg_con.items():
        # print(key, val)
        # print("Out deg")
        # for key, val in out_deg_con.items():
        # print(key, val)

        # clust_coefs = nx.clustering(self.g)
        # for i in clust_coefs.values():
        # print(i)
        # print("Mean len: ", nx.average_shortest_path_length(self.dig))
        # print("Diameter ", nx.diameter(self.g))

        to_remove_rand = random.sample(self.g.nodes, 100)
        #self.delete_max([(0, v) for v in to_remove_rand])
        #self.delete_max(max_in)
        self.delete_max(max_out)

        # print("Clustering coefficient:", nx.average_clustering(self.g))
