# 2021 Day 2: Dive!
#boilerplate to read in input file
f = open('aoc02.txt','rt')
raw_input = []


for line in f:
    raw_input += [line[:-1]]
f.close()

# Part 1 - simple x and y tracking
x = 0
y = 0
for line in raw_input:
    split_line = line.split(' ')
    if split_line[0] == 'forward':
        x += int(split_line[1])
    elif split_line[0] == 'down':
        y += int(split_line[1])
    elif split_line[0] == 'up':
        y -= int(split_line[1])
print('Part 1: x = ' + str(x) + ', y = ' + str(y) + ', solution = ' + str(x * y))

# Part 2 - now up and down modify the aim, forward also changes depth
x = 0
y = 0
aim = 0
for line in raw_input:
    split_line = line.split(' ')
    if split_line[0] == 'forward':
        x += int(split_line[1])
        y += int(split_line[1]) * aim
    elif split_line[0] == 'down':
        aim += int(split_line[1])
    elif split_line[0] == 'up':
        aim -= int(split_line[1])
print('Part 2: x = ' + str(x) + ', y = ' + str(y) + ', aim = ' + str(aim) + ', solution = ' + str(x * y))