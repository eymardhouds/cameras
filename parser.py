import math

def get_distances(points):
    distances={}
    for point1 in points:
        for point2 in points:
            if point1!=point2:
                square_dist=math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2)
                distances[point1]=math.sqrt(square_dist)
                print(distances[point1])
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
    
