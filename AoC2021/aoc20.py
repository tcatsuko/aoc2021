f = open('aoc20.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
algorithm = raw_input[0]

# Build up the image, put a buffer of 2 pixels per loop on each edge
# PART 1

image = []
num_of_loops = 2
buffer = num_of_loops * 2
for line in raw_input[2:]:
    current_line = '0' * buffer
    buffer_lines = len(current_line)
    for character in line:
        if character == '.':
            current_line += '0'
        else:
            current_line += '1'
    current_line += '0' * buffer
    image += [current_line]
image_width = len(image[0])
vert_buffer = ''
for x in range(image_width):
    vert_buffer += '0'
for x in range(buffer):
    image.insert(0, vert_buffer)
    image.append(vert_buffer)


num_of_loops = 2
first_loop = False
for counter in range(num_of_loops):
    if counter % 2 == 0: # based on analysis of the actual program input
        oob = '0'
    else:
        oob = '1'

    new_image = []
    for y in range(0, len(image)):
        new_row = ''
        for x in range(0, len(image[0])):
            string_value = ''
            if x == 298:
                test1 = len(image[0])
            if y > 0 and x > 0 and y < len(image)-1 and x < len(image[0])-1:
                string_value += image[y-1][x-1:x+2]
                string_value += image[y][x-1:x+2]
                string_value += image[y+1][x-1:x+2]
            elif y == 0 and x > 0 and x < len(image[0])-1: # top row not left or right edge
                string_value += oob + oob + oob
                string_value += image[y][x-1:x+2]
                string_value += image[y+1][x-1:x+2]
            elif y == len(image) - 1 and x > 0 and x < len(image[0])-1: # bottom row not left or right edge
                string_value += image[y-1][x-1:x+2]
                string_value += image[y][x-1:x+2]
                string_value += oob + oob + oob
            elif y > 0 and y < len(image) - 1 and x == 0: # left edge
                string_value += oob + image[y - 1][x:x+2]
                string_value += oob + image[y][x:x+2]
                string_value += oob + image[y+1][x:x+2]
            elif y > 0 and y < len(image) - 1 and x == len(image[0])-1: # right edge
                string_value = image[y-1][x-1:x+1] + oob
                string_value = image[y][x-1:x+1] + oob
                string_value = image[y+1][x-1:x+1] + oob
            elif y == 0 and x == 0: # top left
                string_value += oob + oob + oob
                string_value += oob + image[y][x:x+2]	
                string_value += oob + image[y+1][x:x+2]
            elif y == 0 and x == len(image[0]) - 1:    # top right
                string_value += oob + oob + oob
                string_value += image[y][x-1:x+1] + oob
                string_value += image[y+1][x-1:x+1] + oob
            elif y == len(image)-1 and x == 0:  #bottom left
                string_value += oob + image[y-1][x:x+2]
                string_value += oob + image[y][x:x+2]
                string_value += oob + oob + oob
            elif y == len(image) - 1 and x == len(image[0]) - 1:
                string_value += image[y-1][x-1:x+1] + oob
                string_value += image[y][x-1:x+1] + oob
                string_value += oob + oob + oob
            binary_value = int(string_value, 2)
            applied_rule = algorithm[binary_value]
            if applied_rule == '#':
                new_row += '1'
            else:
                new_row += '0'
        new_image += [new_row]
    image = new_image

# Count up the lit pixels
current_sum = 0
# Seems to create corruption near edges, so removing half of the buffer
for line in image[num_of_loops:-num_of_loops]:
    current_sum += line[num_of_loops:-num_of_loops].count('1')
print('Part 1: sum of lit pixels is ' + str(current_sum))

# ************ Part 2

image = []
num_of_loops = 50
buffer = num_of_loops * 2
for line in raw_input[2:]:
    current_line = '0' * buffer
    buffer_lines = len(current_line)
    for character in line:
        if character == '.':
            current_line += '0'
        else:
            current_line += '1'
    current_line += '0' * buffer
    image += [current_line]
image_width = len(image[0])
vert_buffer = ''
for x in range(image_width):
    vert_buffer += '0'
for x in range(buffer):
    image.insert(0, vert_buffer)
    image.append(vert_buffer)


num_of_loops = 50
first_loop = False
for counter in range(num_of_loops):
    if counter % 2 == 0: # based on analysis of the actual program input
        oob = '0'
    else:
        oob = '1'

    new_image = []
    for y in range(0, len(image)):
        new_row = ''
        for x in range(0, len(image[0])):
            string_value = ''
            if x == 298:
                test1 = len(image[0])
            if y > 0 and x > 0 and y < len(image)-1 and x < len(image[0])-1:
                string_value += image[y-1][x-1:x+2]
                string_value += image[y][x-1:x+2]
                string_value += image[y+1][x-1:x+2]
            elif y == 0 and x > 0 and x < len(image[0])-1: # top row not left or right edge
                string_value += oob + oob + oob
                string_value += image[y][x-1:x+2]
                string_value += image[y+1][x-1:x+2]
            elif y == len(image) - 1 and x > 0 and x < len(image[0])-1: # bottom row not left or right edge
                string_value += image[y-1][x-1:x+2]
                string_value += image[y][x-1:x+2]
                string_value += oob + oob + oob
            elif y > 0 and y < len(image) - 1 and x == 0: # left edge
                string_value += oob + image[y - 1][x:x+2]
                string_value += oob + image[y][x:x+2]
                string_value += oob + image[y+1][x:x+2]
            elif y > 0 and y < len(image) - 1 and x == len(image[0])-1: # right edge
                string_value = image[y-1][x-1:x+1] + oob
                string_value = image[y][x-1:x+1] + oob
                string_value = image[y+1][x-1:x+1] + oob
            elif y == 0 and x == 0: # top left
                string_value += oob + oob + oob
                string_value += oob + image[y][x:x+2]	
                string_value += oob + image[y+1][x:x+2]
            elif y == 0 and x == len(image[0]) - 1:    # top right
                string_value += oob + oob + oob
                string_value += image[y][x-1:x+1] + oob
                string_value += image[y+1][x-1:x+1] + oob
            elif y == len(image)-1 and x == 0:  #bottom left
                string_value += oob + image[y-1][x:x+2]
                string_value += oob + image[y][x:x+2]
                string_value += oob + oob + oob
            elif y == len(image) - 1 and x == len(image[0]) - 1:
                string_value += image[y-1][x-1:x+1] + oob
                string_value += image[y][x-1:x+1] + oob
                string_value += oob + oob + oob
            binary_value = int(string_value, 2)
            applied_rule = algorithm[binary_value]
            if applied_rule == '#':
                new_row += '1'
            else:
                new_row += '0'
        new_image += [new_row]
    image = new_image

# Count up the lit pixels
current_sum = 0
# Seems to create corruption near edges, so removing half of the buffer
for line in image[num_of_loops:-num_of_loops]:
    current_sum += line[num_of_loops:-num_of_loops].count('1')
print('Part 2: sum of lit pixels is ' + str(current_sum))
# 18597 too high
