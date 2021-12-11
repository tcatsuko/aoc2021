f = open('aoc11.txt','rt')
oc_grid = []
for line in f:
    oc_grid += [[int(x) for x in line[:-1]]]
f.close()

# Add a border to make things easier.  Thanks, day 9!
for line in oc_grid:
    line.insert(0, -500000000)
    line.append(-500000000)
top = [-500000000] * len(oc_grid[0])
oc_grid.insert(0,top)
oc_grid.append(top)

# Part 1 and 2
passes = 1000000
flash_counter = 0
sync = False
sync_step = 0
for step in range(passes):
    # First, increment everything
    for idx, line in enumerate(oc_grid):
        line = [x+1 for x in line]
        oc_grid[idx] = line
    new_flashes = True
    step_flashes = set()
    
    while new_flashes == True:
        new_flashes = False
        # Now we loop through and determine flashes
        for y in range(1, len(oc_grid) - 1):
            for x in range(1, len(oc_grid[0]) - 1):
                if oc_grid[y][x] > 9:
                    if (x, y) not in step_flashes:
                        step_flashes.add((x, y))
                        flash_counter += 1
                        new_flashes = True
                        # Increase neighbors
                        oc_grid[y-1][x-1] += 1
                        oc_grid[y-1][x] += 1
                        oc_grid[y-1][x+1] += 1
                        oc_grid[y][x+1] += 1
                        oc_grid[y+1][x+1] += 1
                        oc_grid[y+1][x] += 1
                        oc_grid[y+1][x-1] += 1
                        oc_grid[y][x-1] += 1
    # Now we set everything over 10 to 0
    for idx, line in enumerate(oc_grid):
        new_line = []
        for number in line:
            if number > 9:
                new_line += [0]
            elif number < 0:
                new_line += [-500000000]
            else:
                new_line += [number]
        oc_grid[idx] = new_line
        
    # Now see if things are synchronized
    sync = True
    for line in oc_grid:
        for number in line:
            if number > 0:
                sync = False
    if sync == True:
        sync_step = step + 1
        break
    if step == 99:
        print('Part 1: there have been ' + str(flash_counter) + ' flashes after ' + str(step + 1) + ' passes.')
    
print('Part 2: synchronization happens on step ' + str(sync_step))