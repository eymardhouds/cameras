import math
import time



class Camera:

    def __init__(self, price, coord, efficiency, cover_list):
        self.price = price
        self.coord = coord
        self.efficiency = efficiency
        self.cover_list = cover_list
        self.active = False

class Museum:
    """
    La classe Museum prend deux params en intialisation:
    - Une largeur de quadrillage
    - Un fichier d'input comme input_9.txt
    Cette classe possede une méthode solve qui donne une bonne approximation du problème de la surveillance du musée
    """
    def __init__(self, epsilon, file):
        """
        Initialisation du problème: on lit les données en input et on définit les variables principales
        """

        with open(file, 'r') as doc:
            content = doc.readlines()
        content = [x.strip() for x in content]
        self.p_dist = int(content[0].split(',')[0])
        self.g_dist = int(content[0].split(',')[1])
        self.p_price = int(content[1].split(',')[0])
        self.g_price = int(content[1].split(',')[1])
        self.oeuvre = {}
        for line in content[2:]:
            self.oeuvre[(int(line.split(',')[0]), int(line.split(',')[1]))] = [False, []]

        self.id = 0
        self.epsilon = epsilon

        self.present_cameras = []

        self.absent_cameras = self.get_cameras(self.p_price)
        self.absent_cameras += self.get_cameras(self.g_price)

        self.total_cost = 0

        print("Epsilon = %.1f" % self.epsilon)
        print("L = %.1f" % self.L)
        print("l = %.1f" % self.l)


    def get_cameras(self, price):
        """
        On créé une liste de cameras que l'on pourrait potentiellement poser aux coins de chacune des cases de notre quadrillage
        """
        cameras = []

        rank_x = sorted([x[0] for x in self.oeuvre])
        self.max_x = rank_x[-1]
        self.min_x = rank_x[0]
        self.L = abs(self.max_x - self.min_x)

        rank_y = sorted([y[1] for y in self.oeuvre])
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
        """
        Cette fonction ajoute les caméras une à une en prenant celle qui minimise l'augmentation du cout total.
        Une fois une caméra ajoutée, on note les tableaux que l'on surveille à présent et on update les densités des caméras restantes
        On s'arrête lorsque tous les tableaus (self.to_cover) sont surveillés
        """
        self.to_cover = len(self.oeuvre)

        while self.to_cover > 0:
            print("sorting...")
            self.absent_cameras.sort(key=lambda x: x.efficiency, reverse=True)
            camera = self.absent_cameras.pop(0)
            camera.active = True
            self.total_cost += camera.price
            self.present_cameras.append(camera)
            for i in camera.cover_list:
                self.to_cover -= 1
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
        """
        On check si la norme euclidienne d'un tableau à une caméras est comprise dans le rayon d'action de celle ci
        """
        if pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) <= pow(range,2):
            return True
        return False

    def set_camera(self, xc, yc, price):
        """
        Lors de l'installation d'une camera on calcule son efficacité, c'est à dire le nombre de tableaux qu'elle est capable de surveiller

        """
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
                        coverefficiency += 1
                        cover_list += [(x,y)]
                        self.oeuvre[(x,y)][1].append(camera)

        camera.efficiency = coverefficiency /price
        camera.cover_list = cover_list

        print("camera set")
        return camera


    def write_result(self, file_name):
        """
        Cette fonction affiche les résultats et les écris dans un fichier propre de soumission prêt à être posté en ligne

        """
        result = ""

        for camera in self.present_cameras:
            result += (str(camera.price) + "," + str(camera.coord)[1:-1] + "\n")

        with open(file_name, "w") as result_file:
            result_file.write(result)

if __name__ == '__main__':

    start = time.time()
    museum = Museum(2, 'input_9.txt')
    stop1 = time.time()
    museum.first_solve()
    stop2 = time.time()
    print("Cost = " + str(museum.total_cost))
    print("Init time = ", stop1 - start)
    print("Solving time = ", stop2 - stop1)
    print("Execution time = ", stop2 - start)
    museum.write_result("result2.txt")


