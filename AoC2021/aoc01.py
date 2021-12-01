#boilerplate to read in input file
f = open('aoc01.txt','rt')
raw_input = []
for line in f:
    raw_input += [int(line[:-1])]
f.close()

# part 1
depth_increase = 0
for x in range(1,len(raw_input)):
    if raw_input[x-1] < raw_input[x]:
        depth_increase += 1
print("Part 1: " + str(depth_increase))

# part 2
# Calculate sliding sums, save in new array
sliding_window = []
for x in range(0, len(raw_input) - 2):
    sliding_window += [raw_input[x] + raw_input[x + 1] + raw_input[x + 2]]
depth_increase2 = 0
for x in range(1, len(sliding_window)):
    if sliding_window[x-1] < sliding_window[x]:
        depth_increase2 += 1
print("Part 2: " + str(depth_increase2))