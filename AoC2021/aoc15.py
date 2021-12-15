import networkx as nx

f = open('aoc15.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

risk_map = []
for line in raw_input:
    current_line = [int(x) for x in line]
    risk_map += [current_line]
# let's do like other days and add a border
width = len(risk_map[0])
height = len(risk_map)

risk_map.insert(0, [999999999999999] * width)
risk_map.append([999999999999999] * width)
for line in risk_map:
    line.insert(0, 999999999999999)
    line.append(999999999999999)
print()
start_pos = (1, 1)
end_pos = (width, height)

G = nx.DiGraph()

for y in range(height + 1):
    for x in range(width + 1):
        current_point = (x, y)
        up_weight = risk_map[y - 1][x]
        right_weight = risk_map[y][x + 1]
        down_weight = risk_map[y + 1][x]
        left_weight = risk_map[y][x - 1]
        G.add_edge((x, y),(x, y-1), weight=up_weight)
        G.add_edge((x, y), (x + 1, y), weight=right_weight)
        G.add_edge((x, y),(x, y+1), weight=down_weight)
        G.add_edge((x, y), (x-1, y), weight=left_weight)
        
short_path = nx.shortest_path(G, source=start_pos, target=end_pos, weight='weight')
short_path_list = list(short_path)

# Calculate the total risk, do not count the first point
total_risk = 0
for point in short_path_list[1:]:
    x = point[0]
    y = point[1]
    total_risk += risk_map[y][x]
print('Part 1: total risk is ' + str(total_risk))

# need to build a new map for part 2
# So pretty much do this all over again.

risk_map = []

for line in raw_input: # Going to get at least the first row done
    current_line = [int(x) for x in line]
    original_line = current_line[:]
    for i in range(1,5):
        #new_addition = [x+i if x + i < 10 else 1+i-1 for x in original_line]
        new_addition = [(x + i) % 9 if (x + i) > 9 else x + i for x in original_line]
        current_line += new_addition
    risk_map += [current_line]
# Now do that 4 more times
added_risk = []
for i in range(1, 5):
    for line in risk_map:
        #new_line = [x + 1 if x + i < 10 else 1+i-1 for x in line]
        new_line = [(x + i) % 9 if (x + i) > 9 else x + i for x in line]
        added_risk += [new_line]
risk_map += added_risk

width = len(risk_map[0])
height = len(risk_map)

risk_map.insert(0, [999999999999999] * width)
risk_map.append([999999999999999] * width)
for line in risk_map:
    line.insert(0, 999999999999999)
    line.append(999999999999999)
start_pos = (1, 1)
end_pos = (width, height)

G = nx.DiGraph()

for y in range(height + 1):
    for x in range(width + 1):
        current_point = (x, y)
        up_weight = risk_map[y - 1][x]
        right_weight = risk_map[y][x + 1]
        down_weight = risk_map[y + 1][x]
        left_weight = risk_map[y][x - 1]
        G.add_edge((x, y),(x, y-1), weight=up_weight)
        G.add_edge((x, y), (x + 1, y), weight=right_weight)
        G.add_edge((x, y),(x, y+1), weight=down_weight)
        G.add_edge((x, y), (x-1, y), weight=left_weight)
        
short_path = nx.shortest_path(G, source=start_pos, target=end_pos, weight='weight')
short_path_list = list(short_path)

# Calculate the total risk, do not count the first point
total_risk = 0
for point in short_path_list[1:]:
    x = point[0]
    y = point[1]
    total_risk += risk_map[y][x]
print('Part 2: total risk is ' + str(total_risk))

