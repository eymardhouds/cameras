import math

# On définit un quadrillage au maillage epsilon et on fait varier (x_max-x_min)/epsilon
# Puis itérativement:
    # On calcule la densité de tableaux surveillés par camera , par type de camera (appelé matrice de densité, density_matrice)
    # On selectionne le max et on retire les cameras, on update la matrice de densité
    # Arrêt de la boucle for: quand tous les tableaux sont surveillés

# (On répète plusieurs fois et on sélectionne la meilleure réponse)
# idée: un facteur température: on commence par placer des cameras au hasard puis on fait notre algo

def get_distances(points):
    distances={}
    for point1 in points:
        distances[point1]={}
        for point2 in points:
            distances[point1][point2]={}
            if point1!=point2:
                square_dist=math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2)
                distances[point1][point2]=math.sqrt(square_dist)
    return distances

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
        distances=get_distances(oeuvres)

        first_point=random.choice(oeuvres)
        visited=[first_point]
        for i in range (2,30):
            min_dist=0
