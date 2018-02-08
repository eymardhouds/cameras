import math
from pyscipopt import Model, quicksum, multidict
import time


class Museum:

    def __init__(self, epsilon, file):
        #self.distances = get_distnaces(oeuvres)

        with open(file, 'r') as doc:
            content = doc.readlines()
        content = [x.strip() for x in content]
        self.p_dist = int(content[0].split(',')[0])
        self.g_dist = int(content[0].split(',')[1])
        self.p_price = int(content[1].split(',')[0])
        self.g_price = int(content[1].split(',')[1])
        self.oeuvres = []
        for line in content[2:]:
            self.oeuvres.append((int(line.split(',')[0]), int(line.split(',')[1])))

        self.epsilon = epsilon
        print(self.p_dist)
        print(self.oeuvres)

        self.model = Model("Camera")

        self.quadrillage_p = self.get_quadrillage("p")
        self.quadrillage_g = self.get_quadrillage("g")

        self.model.setObjective(quicksum(self.quadrillage_g[i] for i in self.quadrillage_g.keys()) * self.g_price +
                                quicksum(self.quadrillage_p[i] for i in self.quadrillage_p.keys()) * self.p_price, "minimize")

        print(self.quadrillage_p)

    def get_quadrillage(self, id):

        self.quadrillage = {}

        print("Epsilon = %.1f" % self.epsilon)
        rank_x = sorted([x[0] for x in self.oeuvres])
        self.max_x = rank_x[-1]
        self.min_x = rank_x[0]
        self.L = abs(self.max_x - self.min_x)

        print("L = %.1f" % self.L)

        rank_y = sorted([y[1] for y in self.oeuvres])
        self.max_y = rank_y[-1]
        self.min_y = rank_y[0]
        self.l = abs(self.max_y - self.min_y)

        print("l = %.1f" % self.l)

        id = 0
        for x in range(self.min_x, self.max_x + self.epsilon, self.epsilon):
            for y in range(self.min_y, self.max_y + self.epsilon, self.epsilon):
                id += 1
                self.quadrillage[x,y] = (self.model.addVar(str(id), vtype="B"))

        return self.quadrillage

    def add_constraints(self):
        for o in self.oeuvres:
            cam_list = self.fetch_close_cam(o)
            self.model.addCons(quicksum(cam_list[i] for i in range(len(cam_list))) >= 1, "present camera")

    def solve(self):
        self.model.optimize()

    def _xvalues(self, x0, dist):

        xvalues = []
        difx = (x0 - dist - self.min_x) % self.epsilon
        x = max(x0 - difx - dist, self.min_x)
        while x <= self.max_x and x <= x0 + dist:
            xvalues.append(x)
            x += self.epsilon

        return xvalues

    def _yvalues(self, y0, dist):

        yvalues = []
        difx = (y0 - dist - self.min_y) % self.epsilon
        y = max(y0 - difx - dist, self.min_y)
        yvalues.append(y)
        while y <= self.max_y and y <= y0 + dist:
            yvalues.append(y)
            y += self.epsilon

        return yvalues

    def fetch_close_cam(self, o):

        camera_list = []

        xvalues = self._xvalues(o[0], self.g_dist)
        yvalues = self._yvalues(o[1], self.g_dist)
        for x in xvalues:
            for y in yvalues:
                camera_list.append(self.quadrillage_g[x,y])

        xvalues = self._xvalues(o[0], self.p_dist)
        yvalues = self._yvalues(o[1], self.p_dist)
        for x in xvalues:
            for y in yvalues:
                camera_list.append(self.quadrillage_p[x, y])

        return camera_list


if __name__ == '__main__':
    start = time.time()
    museum = Museum(1, 'input_9.txt')
    museum.add_constraints()
    museum.solve()
    stop = time.time()
    print("Execution time = ", stop - start)

