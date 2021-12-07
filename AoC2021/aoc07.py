# AoC 2021 Day 7: The Treachery of Whales

f = open('aoc07.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
crabs = [int(x) for x in raw_input[0].split(',')]

fuel_1 = []
for x in range(max(crabs) + 1):
    current_fuel = 0
    for other_crab in crabs:
        current_fuel += abs(other_crab - x)
    fuel_1 += [current_fuel]
print('Part 1: minimum fuel used is ' + str(min(fuel_1)))

fuel_2 = []
for x in range(max(crabs) + 1):
    current_fuel = 0
    for other_crab in crabs:
        distance = abs(other_crab - x)
        current_fuel += int((distance * (1 + distance) / 2))
    fuel_2 += [current_fuel]
print('Part 2: minimum fuel used is ' + str(min(fuel_2)))