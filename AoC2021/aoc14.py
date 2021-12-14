f = open('aoc14.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

initial_molecule = raw_input[0]
letter_count = {}
for letter in initial_molecule:
    if letter not in letter_count:
        letter_count[letter] = 1
    else:
        letter_count[letter] += 1

rules = {}
added_letters = {}
for line in raw_input[2:]:
    split_line = line.split(' -> ')
    if split_line[0] not in added_letters:
        added_letters[split_line[0]] = split_line[1]
    
    left_side = split_line[0][0] + split_line[1]
    right_side = split_line[1] + split_line[0][1]
    rules[split_line[0]] = (left_side, right_side)
print()

# Get initial pairs
pairs = {}
for idx, char in enumerate(initial_molecule[:-1]):
    pair = char + initial_molecule[idx + 1]
    if pair not in pairs:
        pairs[pair] = 1
    else:
        pairs[pair] += 1

# Let's build a polymer!
steps = 40
for step in range(steps):
    new_pairs = {}
    
    for pair in pairs:
        num_to_replace = pairs[pair]
        replacements = rules[pair]
        added_letter = added_letters[pair]
        if added_letter not in letter_count:
            letter_count[added_letter] = num_to_replace
        else:
            letter_count[added_letter] += num_to_replace
        if replacements[0] not in new_pairs:
            new_pairs[replacements[0]] = num_to_replace
        else:
            new_pairs[replacements[0]] += num_to_replace
        if replacements[1] not in new_pairs:
            new_pairs[replacements[1]] = num_to_replace
        else:
            new_pairs[replacements[1]] += num_to_replace        
    pairs = new_pairs

    # Now count elements:
    max_letter = max(letter_count.values())
    min_letter = min(letter_count.values())
    if step == 9:
        print('Part 1: after 10 steps most common - least common elements is ' + str(max_letter - min_letter))
print('Part 2: after 40 steps most common - least common elements is ' + str(max_letter - min_letter))