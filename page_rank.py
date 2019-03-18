import operator
import os

import networkx as nx
import numpy as np


class PageRank:
    ITER = 500
    STOP_F = 1.0e-6
    FILENAME = "page_rank.txt"

    def __init__(self, G: nx.DiGraph, direc):
        self.file_path = os.path.join(direc, self.FILENAME)
        self.g = G
        self.x = {}

    def check_concur(self):
        d_min = 0.1
        d_step = 0.05
        d_max = 1

        d_max += d_step
        for d_i in np.arange(d_min, d_max, d_step):
            it = self.calc_page_rank(d_i)
            print("d=%f: %d" % (d_i, it))
        nx.pagerank(self.g)

    def calc_page_rank(self, d=1.0):
        n = self.g.number_of_nodes()
        self.x = {v: 1 / n for v in self.g.nodes}
        dangling_nodes = [n for n in self.g if self.g.out_degree(n) == 0.0]
        dangling_p = dict(self.x)
        other_site_p = dangling_p
        for _ in range(self.ITER):
            tmp = dict(self.x)
            danglesum = d * sum(tmp[n] for n in dangling_nodes)
            for vi in self.g.nodes:
                p = list(self.g.predecessors(vi))
                result = 0
                for vj in p:
                    rj = tmp[vj]
                    lj = self.g.out_degree(vj)
                    result += rj / lj
                result *= d
                result += danglesum * dangling_p.get(vi, 0) + (1.0 - d) * other_site_p.get(vi, 0)
                self.x[vi] = result
            err = sum([abs(self.x[n] - tmp[n]) for n in self.x])
            if err < n * self.STOP_F:
                return _
        return self.ITER

    def print(self, top_c=10):
        sorted_x = sorted(self.x.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(top_c):
            print(sorted_x[i])

    def save(self):
        sorted_x = sorted(self.x.items(), key=operator.itemgetter(1), reverse=True)
        with open(self.file_path, "w") as f:
            for xi in sorted_x:
                f.write("pr: %f %s\n" % (xi[1], xi[0]))
        print("Page ranks saved at: %s" % self.file_path)
