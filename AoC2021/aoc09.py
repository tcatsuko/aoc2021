f = open('aoc09.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
heightmap = []

for line in raw_input:
    heightmap += [[int(x) for x in line]]
    
# Add border of 9s, will help in part 2
for x in range(len(heightmap)):
    heightmap[x].append(9)
    heightmap[x].insert(0,9)
heightmap.append([9] * len(heightmap[0]))
heightmap.insert(0, [9] * len(heightmap[0]))

# Part 1
risk_level = 0
low_points = []
for y in range(len(heightmap)):
    for x in range(len(heightmap[y])):
        max_neighbors = 4
        higher_neighbors = 0
        current_number = heightmap[y][x]
        # check up
        if y > 0:
            if heightmap[y-1][x] > current_number:
                higher_neighbors += 1
        else:
            max_neighbors -= 1
        
        # Check right
        if x < (len(heightmap[y]) - 1):
            if heightmap[y][x + 1] > current_number:
                higher_neighbors += 1
        else:
            max_neighbors -= 1
        
        # Check down
        if y < (len(heightmap) - 1):
            if heightmap[y + 1][x] > current_number:
                higher_neighbors += 1
        else:
            max_neighbors -= 1
            
        # Check left
        if x > 0:
            if heightmap[y][x-1] > current_number:
                higher_neighbors += 1
        else:
            max_neighbors -= 1
        
        # Put it all together
        if higher_neighbors == max_neighbors:
            # It's a low point
            risk_level += current_number + 1
            low_points += [(x, y)]

print('Part 1: risk level is ' + str(risk_level))

visited_points = []
basin_sizes = []
for low_point in low_points:
    visited_points = set()
    points_to_visit = []
    points_to_visit += [low_point]
    
    while len(points_to_visit) != 0:
        current_point = points_to_visit[0]
        points_to_visit.remove(current_point)
        visited_points.add(current_point)
        x = current_point[0]
        y = current_point[1]
        above_point = (x, y - 1)
        if (above_point not in visited_points) and heightmap[y-1][x] < 9:
            points_to_visit += [(x, y-1)]
        right_point = (x + 1, y)
        if (right_point not in visited_points) and heightmap[y][x+1] < 9:
            points_to_visit += [(x+1, y)]
        below_point = (x, y + 1)
        if (below_point not in visited_points) and heightmap[y+1][x] < 9:
            points_to_visit += [(x, y+1)]
        left_point = (x - 1, y)
        if (left_point not in visited_points) and heightmap[y][x-1] < 9:
            points_to_visit += [(x-1, y)]
    basin_sizes += [len(visited_points)]

basin_sizes.sort()
largest_basins = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
print('Part 2: product of three largest basin sizes is ' + str(largest_basins))
