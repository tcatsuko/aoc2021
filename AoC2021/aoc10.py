f = open('aoc10.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

# Parse the lines
def reduce_line(line):
    current_line = line
    pairs = ['()', '[]', '{}', '<>']
    for item in pairs:
        current_line = current_line.replace(item, '')
    if current_line == line:
        return line
    else:
        return reduce_line(current_line)
    
    
incomplete_lines = []
corrupted_lines = []

closings = [']', ')', '}', '>']
for idx, line in enumerate(raw_input):

    cleaned_line = reduce_line(line)
    corrupted_line = False
    for item in closings:
        if item in cleaned_line:
            corrupted_line = True
    if corrupted_line == True:
        corrupted_lines += [cleaned_line]
    else:
        incomplete_lines += [cleaned_line]

# Part 1
corrupted_points = {')': 3, ']':57, '}': 1197, '>':25137}
part1_points = 0
for line in corrupted_lines:
    first_corrupt = False
    for letter in line:
        if (letter in closings) and (first_corrupt == False):
            first_corrupt = True
            part1_points += corrupted_points[letter]
print('Part 1: points from corruption: ' + str(part1_points))

# Part 2
incomplete_points = {')': 1, ']':2, '}': 3, '>':4}
part2_points = []
closings_dict = {'(':')', '[':']', '{':'}', '<':'>'}
for line in incomplete_lines:
    score = 0
    reversed_line = line[::-1]
    for character in reversed_line:
        closing = closings_dict[character]
        score *= 5
        score += incomplete_points[closing]
    part2_points += [score]
part2_points.sort()
print('Part 2: points from corruption: ' + str(part2_points[int(len(part2_points)/2)]))
