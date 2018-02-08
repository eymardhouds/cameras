import math
from pyscipopt import Model, quicksum, multidict
import time


class Camera:

    def __init__(self, price, coord, efficiency, cover_list):
        self.price = price
        self.coord = coord
        self.efficiency = efficiency
        self.cover_list = cover_list
        self.active = False

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
        self.non_covered = []
        self.oeuvre = {}
        for line in content[2:]:
            self.oeuvre[(int(line.split(',')[0]), int(line.split(',')[1]))] = (False, [])

        self.id = 0
        self.epsilon = epsilon
        print(self.p_dist)
        print(self.non_covered)

        self.present_cameras = []

        self.absent_cameras = self.get_cameras(self.p_price)
        self.absent_cameras += self.get_cameras(self.g_price)

        print("Epsilon = %.1f" % self.epsilon)
        print("L = %.1f" % self.L)
        print("l = %.1f" % self.l)


    def get_cameras(self, price):

        cameras = []

        rank_x = sorted([x[0] for x in self.non_covered])
        self.max_x = rank_x[-1]
        self.min_x = rank_x[0]
        self.L = abs(self.max_x - self.min_x)

        rank_y = sorted([y[1] for y in self.non_covered])
        self.max_y = rank_y[-1]
        self.min_y = rank_y[0]
        self.l = abs(self.max_y - self.min_y)

        x = self.min_x

        while x <= self.max_x + self.epsilon:
            y = self.min_y
            while y <= self.max_y + self.epsilon:
                cameras.append(self.set_camera(x,y, price))
                y += self.epsilon
            x += self.epsilon

        return cameras


    def first_solve(self):
        self.to_cover = len(self.oeuvre)

        while self.to_cover > 0:
            print("sorting...")
            self.absent_cameras.sort(key=lambda x: x.efficiency, reverse=True)
            camera = self.absent_cameras[0].pop()
            camera.active = True
            self.present_cameras.append(camera)
            for i in camera.cover_list:
                self.oeuvre[i][0] = True
                for c in self.oeuvre[i][1]:
                    if c.active is False:
                        c.efficiency -= 1/c.price
                        c.cover_list.remove(i)

    def _xvalues(self, x0, dist):

        xvalues = []
        x = math.floor(max(x0 - dist, self.min_x))
        while x <= self.max_x and x <= x0 + dist:
            xvalues.append(x)
            x += 1
        return xvalues

    def _yvalues(self, y0, dist):

        yvalues = []
        y = math.floor(max(y0 - dist, self.min_y))
        while y <= self.max_y and y <= y0 + dist:
            yvalues.append(y)
            y += 1
        return yvalues

    def check_l2_dist(self, a, b, range):

        if pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) <= pow(range,2):
            return True
        return False

    def set_camera(self, xc, yc, price):

        camera = Camera(price, (xc,yc), 0, [])
        coverefficiency = 0
        cover_list = []

        if price == 1:
            dist = self.p_dist
        else:
            dist = self.g_dist


        xvalues = self._xvalues(xc, dist)
        yvalues = self._yvalues(yc, dist)

        for x in xvalues:
            for y in yvalues:
                if self.check_l2_dist((x,y), (xc, yc), dist):
                    if (x,y) in self.oeuvre.keys():
                        if self.oeuvre[(x,y)][0] is False:
                            coverefficiency += 1
                            cover_list += [(x,y)]
                            self.oeuvre[(x,y)].append(camera)

        camera.efficiency = coverefficiency /price
        camera.cover_list = cover_list

        return camera

    @property
    def cost(self):

        cost = 0
        for i in self.quadrillage_p.values():
            if self.model.getVal(i):
                cost += self.p_price

        for i in self.quadrillage_g.values():
            if self.model.getVal(i):
                cost += self.g_price

        return cost

    def write_result(self, file_name):

        result = ""

        for coord, valeur in self.quadrillage_p.items():
            if self.model.getVal(valeur)  == True:
                result += ("1" + "," + str(coord[0]) + "," + str(coord[1]) + "\n")

        for coord, valeur in self.quadrillage_g.items():
            if self.model.getVal(valeur)  == True:
                result += ("2" + "," + str(coord[0]) + "," + str(coord[1]) + "\n")

        with open(file_name, "w") as result_file:
            result_file.write(result)

if __name__ == '__main__':
    start = time.time()
    museum = Museum(1, 'input_very_simple.txt')
    museum.first_solve()
    stop = time.time()
    print("Cost = " + str(museum.cost))
    museum.write_result("result2.txt")
    print("Execution time = ", stop - start)


