f = open('aoc13.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

points = []
instructions = []

# read in points and instructions
end_points = False
x_max = 0
y_max = 0
for line in raw_input:
    if line == '':
        end_points = True
        continue
    if end_points == False:
        values = [int(x) for x in line.split(',')]
        points += [(values[0], values[1])]
        if values[0] > x_max:
            x_max = values[0]
        if values[1] > y_max:
            y_max = values[1]
    else:
        instructions += [line.split('along ')[1]]

# build the grid
grid = []
for y in range(y_max + 1):
    blank_row = []
    for x in range(x_max + 1):
        blank_row += [' ']
    grid += [blank_row]
for point in points:
    grid[point[1]][point[0]] = '#'

# Now, time to do the instructions!
for folds, instruction in enumerate(instructions):
    split_instruction = instruction.split('=')
    split_instruction[1] = int(split_instruction[1])
    new_grid = []
    if split_instruction[0] == 'y':
        # Easier one, it's a vertical fold
        fold_line = split_instruction[1]
        new_grid += grid[:split_instruction[1]]
        remainder = grid[split_instruction[1]+1:]
        for idx, line in enumerate(remainder):
            offset = idx + 1
            for idx2, item in enumerate(line):
                if item == '#':
                    new_grid[fold_line - offset][idx2] = item
    
    elif split_instruction[0] == 'x':
        fold_line = split_instruction[1]
        for line in grid:
            new_line = []
            for x in range(fold_line):
                new_line += [line[x]]
            for x in range(fold_line + 1, len(line)):
                offset = x - fold_line
                if line[x] == '#':
                    new_line[fold_line - offset] = '#'
            new_grid += [new_line]
            
    grid = new_grid
    if (folds + 1) == 1:
        num_of_dots = 0
        for line in grid:
            num_of_dots += line.count('#')
        print('Part 1: there are ' + str(num_of_dots) + ' dots visible after 1 fold.')
# Now view the message
print('Part 2 message:')
for line in grid:
    print(''.join(line))
    
