f = open('aoc06.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

fish = []
raw_input = raw_input[0].split(',')
for item in raw_input:
    fish += [int(item)]

fish_generations = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
def count_fish(fish):
    total_counter = 0
    for item in fish:
        total_counter += fish[item]
    return total_counter

for item in fish:
    fish_generations[item] += 1
for day in range(256):
    new_fish_generations = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for item in fish_generations:
        if item == 0:
            new_fish_generations[6] += fish_generations[0]
            new_fish_generations[8] += fish_generations[0]
        else:
            new_fish_generations[item - 1] += fish_generations[item]
    fish_generations = new_fish_generations
    if day == 79:
        print('Part 1: total fish after ' + str(day + 1) + ' days is ' + str(count_fish(fish_generations)))
    elif day == 255:
        print('Part 2: total fish after ' + str(day + 1) + ' days is ' + str(count_fish(fish_generations)))
        