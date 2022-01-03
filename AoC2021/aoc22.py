f = open('aoc22.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

def build_cube(desc, part1 = True):
    decomposed_desc = desc.split(' ')
    cube_type = decomposed_desc[0]
    dimensions = decomposed_desc[1].split(',')
    x = dimensions[0]
    y = dimensions[1]
    z = dimensions[2]
    
    
    x1 = int(x.split('..')[0][2:])
    x2 = int(x.split('..')[1])
    y1 = int(y.split('..')[0][2:])
    y2 = int(y.split('..')[1])
    z1 = int(z.split('..')[0][2:])
    z2 = int(z.split('..')[1])
    if part1 == True:
        # Check and adjust x
        if x1 < -50 and x2 < -50:
            return None
        elif x1 < -50 and x2 >= -50:
            x1 = -50
        if x1 > 50 and x2 > 50:
            return None
        elif x1 <= 50 and x2 > 50:
            x2 = 50
        if x1 < -50 and x2 > 50:
            x1 = -50
            x2 = 50
        # Check and adjust y
        if y1 < -50 and y2 < -50:
            return None
        elif y1 < -50 and y2 >= -50:
            y1 = -50
        if y1 > 50 and y2 > 50:
            return None
        elif y1 <= 50 and y2 > 50:
            y2 = 50
        if y1 < -50 and y2 > 50:
            y1 = -50
            y2 = 50
            
        # check and adjust z
        if z1 < -50 and z2 < -50:
            return None
        elif z1 < -50 and z2 >= -50:
            z1 = -50
        if z1 > 50 and z2 > 50:
            return None
        elif z1 <= 50 and z2 > 50:
            z2 = 50
        if z1 < -50 and z2 > 50:
            z1 = -50
            z2 = 50
    cube = {}
    cube['on'] = True if cube_type == 'on' else False
    cube['x'] = (x1, x2)
    cube['y'] = (y1, y2)
    cube['z'] = (z1, z2)
    return cube

def find_overlap_cuboid(a, b):
    x1 = None
    x2 = None
    y1 = None
    y2 = None
    z1 = None
    z2 = None
    cube = {}
    if b['x'][0] >= a['x'][0] and b['x'][0] <= a['x'][1]:
        x1 = b['x'][0]
    elif a['x'][0] >= b['x'][0] and a['x'][0] <= b['x'][1]:
        x1 = a['x'][0]
    if b['x'][1] >= a['x'][0] and b['x'][1] <= a['x'][1]:
        x2 = b['x'][1]
    elif a['x'][1] >= b['x'][0] and a['x'][1] <= b['x'][1]:
        x2 = a['x'][1]
    if b['y'][0] >= a['y'][0] and b['y'][0] <= a['y'][1]:
        y1 = b['y'][0]
    elif a['y'][0] >= b['y'][0] and a['y'][0] <= b['y'][1]:
        y1 = a['y'][0]
    if b['y'][1] >= a['y'][0] and b['y'][1] <= a['y'][1]:
        y2 = b['y'][1]
    elif a['y'][1] >= b['y'][0] and a['y'][1] <= b['y'][1]:
        y2 = a['y'][1]
    if b['z'][0] >= a['z'][0] and b['z'][0] <= a['z'][1]:
        z1 = b['z'][0]
    elif a['z'][0] >= b['z'][0] and a['z'][0] <= b['z'][1]:
        z1 = a['z'][0]
    if b['z'][1] >= a['z'][0] and b['z'][1] <= a['z'][1]:
        z2 = b['z'][1]
    elif a['z'][1] >= b['z'][0] and a['z'][1] <= b['z'][1]:
        z2 = a['z'][1]
    if x1 and x2 and y1 and y2 and z1 and z2:
        cube['on'] = not b['on']
        cube['x'] = (x1, x2)
        cube['y'] = (y1, y2)
        cube['z'] = (z1, z2)
    return cube

def cubevol(cube):
    volume = (cube['x'][1] - cube['x'][0] + 1) * (cube['y'][1] - cube['y'][0] + 1) * (cube['z'][1] - cube['z'][0] + 1)
    return volume

        
cubes = []
for line in raw_input:
    if build_cube(line):
        cubes += [build_cube(line)]

total_cores = []
for cube in cubes:
    current_list = []
    if cube['on']:
        current_list += [cube]
    for other_cube in total_cores:
        overlap = find_overlap_cuboid(cube, other_cube)
        if overlap:
            current_list += [overlap]
    total_cores += current_list 

total_volume = 0
for cube in total_cores:
    volume = cubevol(cube)
    if cube['on']:
        total_volume += volume
    else:
        total_volume -= volume
print('Part 1: total cores on is ' + str(total_volume))

# Repeat it for part 2, but look at all the cubes
cubes = []
for line in raw_input:
    if build_cube(line, part1 = False):
        cubes += [build_cube(line, part1 = False)]

total_cores = []
for cube in cubes:
    current_list = []
    if cube['on']:
        current_list += [cube]
    for other_cube in total_cores:
        overlap = find_overlap_cuboid(cube, other_cube)
        if overlap:
            current_list += [overlap]
    total_cores += current_list 

total_volume = 0
for cube in total_cores:
    volume = cubevol(cube)
    if cube['on']:
        total_volume += volume
    else:
        total_volume -= volume
        
print('Part 2: total cores on is ' + str(total_volume))

    
