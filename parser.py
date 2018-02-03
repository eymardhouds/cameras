with open('input_9.txt','r') as doc:

            content = doc.readlines()
            content = [x.strip() for x in content]
            p_dist= int(content[0].split(',')[0])
            g_dist = int(content[0].split(',')[1])
            p_price = int(content[1].split(',')[0])
            g_price = int(content[1].split(',')[1])

            oeuvres=[]
            for line in content[2:]:
                oeuvres.append(line.split(','))
