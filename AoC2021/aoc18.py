import itertools
import math
f = open('aoc18.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

def create_snail(my_input):
    value = []
    level = []
    current_level = 0
    for character in my_input:
        if character == '[':
            current_level += 1
        elif character == ']':
            current_level -= 1
        elif character == ',':
            continue
        else:
            value += [int(character)]
            level += [current_level]
    return (value, level)

def explode(snail_number):
    value = snail_number[0][:]
    level = snail_number[1][:]
    
    # find max nested level
    max_next = max(level)
    if max_next < 5: 
        # Nothing left to explode
        return snail_number
    max_index = level.index(max_next)
    # Search left
    left_numbers = level[:max_index]
    right_numbers = level[max_index + 2:]
    has_left = True
    has_right = True
    if left_numbers == []:
        has_left = False
    else:
        left_number = value[max_index - 1] + value[max_index]
    if right_numbers == []:
        has_right = False
    else:
        right_number = value[max_index + 1] + value[max_index + 2]
    if has_left == True:
        value[max_index - 1] = left_number
    if has_right == True:
        value[max_index + 2] = right_number
    value[max_index] = 0
    level[max_index] -= 1
    del value[max_index + 1]
    del level[max_index + 1]
    return(value, level)

def add_snail(snail1, snail2):
    new_value = []
    new_level = []
    new_value = snail1[0][:] + snail2[0][:]
    new_level = [i+1 for i in snail1[1] + snail2[1]]
    return(new_value, new_level)

def split(snail_number):
    high_index = -1
    value = snail_number[0][:]
    level = snail_number[1][:]
    counter = 0
    while counter < len(value):
        if value[counter] > 9:
            high_index = counter
            break
        counter += 1
    if high_index == -1:
        return(value, level)
    left_value = math.floor(value[counter]/2)   
    right_value = math.ceil(value[counter]/2)
    value[counter] = left_value
    level[counter] += 1
    value.insert(counter + 1, right_value)
    level.insert(counter + 1, level[counter])
    return(value, level)

def calculate_magnitude(snail_number):
    value = snail_number[0][:]
    level = snail_number[1][:]
    while len(value) > 1:
        max_level = max(level)
        max_index = level.index(max_level)
        left_mag = 3*value[max_index]
        right_mag = 2*value[max_index + 1]
        magnitude = left_mag + right_mag
        value[max_index] = magnitude
        level[max_index] -= 1
        del value[max_index + 1]
        del level[max_index + 1]
    return value[0]

def reduce_snail(snail_number):
    reduced_number = True
    current_index = 0
    while reduced_number == True:
        check1 = snail_number
        reduced_number = False
        while True:
            check1 = snail_number
            new_snail = explode(snail_number)
            if new_snail[0] == snail_number[0]:
                break
            reduced_number = True
            snail_number = new_snail
            current_index += 1
        new_snail = split(snail_number)
        if new_snail[0] != snail_number[0]:
            current_index += 1
            reduced_number = True
        snail_number = new_snail
        check1 = snail_number
    return snail_number

    
snail_number = create_snail(raw_input[0])    
for snail_text in raw_input[1:]:
    next_number = create_snail(snail_text)
    snail_number = add_snail(snail_number, next_number)
    snail_number = reduce_snail(snail_number)



magnitude = calculate_magnitude(snail_number)
print('Part 1: magnitude of homework problem is ' + str(magnitude))


perm_list = [x + y for x, y in itertools.permutations(raw_input, 2)]
max_magnitude = 0

for line in perm_list:
    snail_line = '[' + line + ']'
    snail_number = create_snail(snail_line)
    snail_number = reduce_snail(snail_number)
    magnitude = calculate_magnitude(snail_number)
    if magnitude > max_magnitude:
        max_magnitude = magnitude
print('Part 2: maximum magnitude is ' + str(max_magnitude))
