f = open('aoc25.txt','rt')
seafloor = []
for line in f:
    current_line = []
    for character in line[:-1]:
        current_line += [character]
    seafloor += [current_line]
f.close()
y_max = len(seafloor)
x_max = len(seafloor[0])

steps = 0
moved = True
while moved == True:
    steps += 1
    moved = False
    # build new blank floor
    #new_floor = []
    #for y in range(y_max):
        #new_row = ['.'] * x_max
        #new_floor += [new_row]
    # move right first
    new_floor = []
    for row in seafloor:
        new_floor += [row[:]]

    for y in range(y_max):
        for x in range(x_max):
            current_tile = seafloor[y][x]
            next_tile = seafloor[y][x+1] if x < x_max - 1 else seafloor[y][0]
            if next_tile == '.' and current_tile == '>':
                moved = True
                if x < x_max - 1:
                    new_floor[y][x+1] = current_tile
                    new_floor[y][x] = '.'
                else:
                    new_floor[y][0] = current_tile
                    new_floor[y][x] = '.'            
    seafloor = new_floor[:]
    new_floor = []
    for row in seafloor:
        new_floor += [row[:]]
    
    # move down next
    for y in range(y_max - 1, -1, -1):
        for x in range(x_max):
            current_tile = seafloor[y][x]
            next_tile = seafloor[y+1][x] if y < y_max - 1 else seafloor[0][x]
            if next_tile == '.' and current_tile == 'v':
                moved = True
                if y < y_max - 1:
                    new_floor[y+1][x] = current_tile
                    new_floor[y][x] = '.'
                else:
                    new_floor[0][x] = current_tile
                    new_floor[y][x] = '.'
    seafloor = new_floor[:]

print('Part 1: it took ' + str(steps) + ' steps to reach a stalemate')