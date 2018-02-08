import math

class museum():

    def __init__(self,epsilon,oeuvres,p_dist,g_dist,p_price,g_price):
        #self.distances = get_distnaces(oeuvres)
        self.p_dist = p_dist
        self.g_dist = g_dist
        self.p_price = p_price
        self.g_price = g_price
        self.oeuvres = oeuvres
        self.epsilon = epsilon
        self.quadrillage=self.get_quadrillage()

    def get_distances(self,oeuvres):
        distances={}
        for point1 in points:
            distances[point1]={}
            for point2 in points:
                distances[point1][point2]={}
                if point1!=point2:
                    square_dist=math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2)
                    distances[point1][point2]=math.sqrt(square_dist)
        return distances

    def get_quadrillage(self):

        self.quadrillage=[]

        print("Epsilon = %.1f" % self.epsilon)
        rank_x=sorted([x[0] for x in self.oeuvres])
        self.max_x = rank_x[-1]
        self.min_x = rank_x[0]
        self.L=abs(self.max_x - self.min_x)

        print("L = %.1f" % self.L)

        rank_y=sorted([y[1] for y in self.oeuvres])
        self.max_y = rank_y[-1]
        self.min_y = rank_y[0]
        self.l=abs(self.max_y-self.min_y)

        print("l = %.1f" % self.l)

        for x in range(0,self.L,self.epsilon):
            for y in range(0,self.l,self.epsilon):
                self.quadrillage.append((x,y))

        return self.quadrillage

    def compute_density(i):
        density=0
        for j in self.oeuvres:
            if self.distance[j][i]<=g_dist:
                density=density+1
        return density

    def initialize_density_matrice():
        density_matrice = {}
        for i in self.quadrillage:
            density_matrice[i]=0

        for i in density_matrice:
            density_matrice[i]=compute_density(i)

        return density_matrice

    def iterate_matrice():
        self.solution = [] # la liste de caméras

        return self.solution

    def solve():


        return solution

if __name__ == '__main__':

    with open('input_9.txt','r') as doc:
        content = doc.readlines()
        content = [x.strip() for x in content]
        p_dist= int(content[0].split(',')[0])
        g_dist = int(content[0].split(',')[1])
        p_price = int(content[1].split(',')[0])
        g_price = int(content[1].split(',')[1])

        oeuvres=[]
        for line in content[2:]:
            oeuvres.append((int(line.split(',')[0]),int(line.split(',')[1])))

        epsilon=1
        m=museum(epsilon,oeuvres,p_dist,g_dist,p_price,g_price)
