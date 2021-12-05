f = open('aoc05.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
dict_points = {}
hv_points = {}
for line in raw_input:
    init_split = line.split(' -> ')
    ep1 = init_split[0].split(',')
    ep2 = init_split[1].split(',')
    if ep1[0] == ep2[0]:
        if int(ep1[1]) < int(ep2[1]):
            for y in range(int(ep1[1]), int(ep2[1]) + 1):
                if (int(ep1[0]), y) not in hv_points:
                    if (int(ep1[0]), y) not in dict_points:
                        dict_points[(int(ep1[0]), y)] = 1
                    else:
                        dict_points[(int(ep1[0]), y)] += 1
                    hv_points[(int(ep1[0]), y)] = 1
                else:
                    dict_points[(int(ep1[0]), y)] += 1
                    hv_points[(int(ep1[0]), y)] += 1
        else:
            for y in range(int(ep2[1]), int(ep1[1]) + 1):
                if (int(ep1[0]), y) not in hv_points:
                    if (int(ep1[0]), y) not in dict_points:
                        dict_points[(int(ep1[0]), y)] = 1
                    else:
                        dict_points[(int(ep1[0]), y)] += 1
                    hv_points[(int(ep1[0]), y)] = 1
                else:
                    dict_points[(int(ep1[0]), y)] += 1
                    hv_points[(int(ep1[0]), y)] += 1
    elif ep1[1] == ep2[1]:
        if int(ep1[0]) < int(ep2[0]):
            for x in range(int(ep1[0]), int(ep2[0]) + 1):
                if (x, int(ep1[1])) not in hv_points:
                    if (x, int(ep1[1])) not in dict_points:
                        dict_points[(x, int(ep1[1]))] = 1
                    else:
                        dict_points[(x, int(ep1[1]))] += 1
                    hv_points[(x, int(ep1[1]))] = 1
                else:
                    dict_points[(x, int(ep1[1]))] += 1
                    hv_points[(x, int(ep1[1]))] += 1
        else:
            for x in range(int(ep2[0]), int(ep1[0]) + 1):
                if (x, int(ep1[1])) not in hv_points:
                    if (x, int(ep1[1])) not in dict_points:
                        dict_points[(x, int(ep1[1]))] = 1
                    else:
                        dict_points[(x, int(ep1[1]))] += 1
                    hv_points[(x, int(ep1[1]))] = 1
                else:
                    dict_points[(x, int(ep1[1]))] += 1 
                    hv_points[(x, int(ep1[1]))] += 1 
    else:
        if int(ep1[0]) < int(ep2[0]):
            if int(ep1[1]) < int(ep2[1]):
                add = 1
            else:
                add = -1
            y = int(ep1[1])
            for x in range(int(ep1[0]), int(ep2[0]) + 1):
                if (x, y) not in dict_points:
                    dict_points[(x,y)] = 1
                else:
                    dict_points[(x,y)] += 1
                y += add
        else:
            if int(ep2[1]) < int(ep1[1]):
                add = 1
            else:
                add = -1
            y = int(ep2[1])
            for x in range(int(ep2[0]), int(ep1[0]) + 1):
                if (x, y) not in dict_points:
                    dict_points[(x,y)] = 1
                else:
                    dict_points[(x,y)] += 1
                y += add                
double_line = 0
for item in hv_points:
    if hv_points[item] > 1:
        double_line += 1
print('Part 1: overlapping line points is ' + str(double_line))
all_points = 0
for item in dict_points:
    if dict_points[item] > 1:
        all_points += 1
print('Part 2: all overlapping line points is ' + str(all_points))

