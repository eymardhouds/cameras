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

        self.id = 0
        self.epsilon = epsilon

        self.model = Model("Camera")

        self.quadrillage_p = self.get_quadrillage()
        self.quadrillage_g = self.get_quadrillage()

        print("Epsilon = %.1f" % self.epsilon)
        print("L = %.1f" % self.L)
        print("l = %.1f" % self.l)

        self.model.setObjective(quicksum(self.quadrillage_g[i] for i in self.quadrillage_g.keys()) * self.g_price +
                                quicksum(self.quadrillage_p[i] for i in self.quadrillage_p.keys()) * self.p_price, "minimize")

    def get_quadrillage(self):

        quadrillage = {}


        rank_x = sorted([x[0] for x in self.oeuvres])
        self.max_x = rank_x[-1]
        self.min_x = rank_x[0]
        self.L = abs(self.max_x - self.min_x)

        rank_y = sorted([y[1] for y in self.oeuvres])
        self.max_y = rank_y[-1]
        self.min_y = rank_y[0]
        self.l = abs(self.max_y - self.min_y)

        x = self.min_x
        y = self.min_y

        while x <= self.max_x + self.epsilon:
            y = self.min_y
            while y <= self.max_y + self.epsilon:
                self.id += 1
                quadrillage[x,y] = (self.model.addVar(str(self.id), vtype="B"))
                y += self.epsilon
            x += self.epsilon

        return quadrillage

    def add_constraints(self):
        for o in self.oeuvres:
            print("adding")
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

    def check_l2_dist(self, a, b, range):

        if pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) <= pow(range,2):
            return True
        return False

    def fetch_close_cam(self, o):

        camera_list = []

        xvalues = self._xvalues(o[0], self.p_dist)
        yvalues = self._yvalues(o[1], self.p_dist)
        for x in xvalues:
            for y in yvalues:
                if self.check_l2_dist(o, (x,y), self.p_dist):
                    camera_list.append(self.quadrillage_p[x, y])


        xvalues = self._xvalues(o[0], self.g_dist)
        yvalues = self._yvalues(o[1], self.g_dist)
        for x in xvalues:
            for y in yvalues:
                if self.check_l2_dist(o, (x,y), self.g_dist):
                    camera_list.append(self.quadrillage_g[x, y])

        return camera_list


    def write_result(self, file_name):

        result = ""

        for coord, valeur in self.quadrillage_p.items():
            if self.model.getVal(valeur)  == True:
                result += ("1" + "," + str(int(coord[0])) + "," + str(int(coord[1])) + "\n")

        for coord, valeur in self.quadrillage_g.items():
            if self.model.getVal(valeur)  == True:
                result += ("2" + "," + str(int(coord[0])) + "," + str(int(coord[1])) + "\n")

        with open(file_name, "w") as result_file:
            result_file.write(result)

if __name__ == '__main__':
    start = time.time()
    museum = Museum(0.5, 'input_9.txt')
    museum.add_constraints()
    stop1 = time.time()
    museum.solve()
    stop2 = time.time()
    print("Init time = ", stop1 - start)
    print("Solving time = ", stop2 - stop1)
    print("Execution time = ", stop2 - start)
    museum.write_result("result.txt")



