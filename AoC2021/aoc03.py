f = open('aoc03.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

# Part 1
# find total amount of numbers
total_inputs = len(raw_input)
# find length of binary number
bin_length = len(raw_input[0])

decomposed_numbers = []
for x in range(bin_length):
    current_bit = []
    for y in range(total_inputs):
        current_bit += [int(raw_input[y][x])]
    decomposed_numbers += [current_bit]
gamma = ''
epsilot = ''
for x in range(len(decomposed_numbers)):
    if sum(decomposed_numbers[x]) > total_inputs/2:
        gamma += '1'
        epsilot += '0'
    else:
        gamma += '0'
        epsilot += '1'
gamma_int = int(gamma, 2)
epsilon_int = int(epsilot, 2)
print('Part 1: power consumption = ' + str(gamma_int * epsilon_int))

# Part 2
oxygen_rating = raw_input[:]
co2_rating = raw_input[:]

for x in range(bin_length):
    temp_o2 = []
    temp_co2 = []
    # Find o2 first
    o2_sum = 0
    if len(oxygen_rating) > 1:
        for item in oxygen_rating:
            if item[x] == '1':
                o2_sum += 1
        if o2_sum >= (float(len(oxygen_rating) )/ 2):
            for item in oxygen_rating:
                if item[x] == '1':
                    temp_o2 += [item]
        else:
            for item in oxygen_rating:
                if item[x] == '0':
                    temp_o2 += [item]
        oxygen_rating = temp_o2[:]
    co2_sum = 0
    if len(co2_rating) > 1:
        for item in co2_rating:
            if item[x] == '1':
                co2_sum += 1
        if co2_sum < (float(len(co2_rating)) / 2):
            for item in co2_rating:
                if item[x] == '1':
                    temp_co2 += [item]
        else:
            for item in co2_rating:
                if item[x] == '0':
                    temp_co2 += [item]
        co2_rating = temp_co2[:]

o2_int = int(oxygen_rating[0], 2)
co2_int = int(co2_rating[0], 2)
print('Part 2: Life Support rating = ' + str(o2_int * co2_int))