import networkx as nx
f = open('aoc12.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

G = nx.Graph()
big_caverns = {}
# Build the graph
for line in raw_input:
    nodes = line.split('-')
    G.add_edge(nodes[0], nodes[1])

def solve(G, current_path, visit_twice):
    current_node = current_path[-1]
    neighbors = G.neighbors(current_node)
    for item in neighbors:
        new_path = current_path + [item]
        if item == 'end':
            yield new_path
        elif item.isupper() or item not in current_path:
            # Can only visit lowercase 
            yield from solve(G, new_path, visit_twice)
        elif visit_twice == True and item != 'start':
            yield from solve(G, new_path, False)
paths_sum = 0
paths_part1 = solve(G, ['start'], False)
for item in paths_part1:
    paths_sum += 1
print('Part 1: there are ' + str(paths_sum) + ' paths.')

paths_part2 = solve(G, ['start'], True)
paths_sum = 0
for item in paths_part2:
    paths_sum += 1
print('Part 2: there are ' + str(paths_sum) + ' paths.')