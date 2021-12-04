f = open('aoc04.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
bingo_numbers = raw_input[0].split(',')

# Helper functions
def id_number(number, bingo_card, bingo_card_tf):
    for x in range(5):
        if number in bingo_card[x]:
            found_index = bingo_card[x].index(number)
            bingo_card[x][found_index] = -1
            bingo_card_tf[x][found_index] = True
            return
def transpose(matrix):
    new_matrix = []
    for x in range(5):
        current_row = []
        current_row += [matrix[0][x]]
        current_row += [matrix[1][x]]
        current_row += [matrix[2][x]]
        current_row += [matrix[3][x]]
        current_row += [matrix[4][x]]
        new_matrix += [current_row]
    #matrix = new_matrix[:]
    return new_matrix
def check_winner(bingo_card_tf):
    # Check rows
    for x in range(5):
        if bingo_card_tf[x] == [True, True, True, True, True]:
            return True
    # Check columns
    temp_card = transpose(bingo_card_tf[:])
    for x in range(5):
        if temp_card[x] == [True, True, True, True, True]:
            return True
    return False
def calculate_score(card):
    score = 0
    for x in range(5):
        current_line = card[x][:]
        current_line = [y if y != -1 else 0 for y in current_line]
        score += sum(current_line)
    return score


# build bingo cards
bingo_cards = []
bingo_cards_tf = []
current_card = []
current_card_tf = []
#for x in range(2, len(raw_input)-1):
del raw_input[0]
del raw_input[0]
del raw_input[-1]
for item in raw_input:
    #current_line = raw_input[x]
    current_line = item
    if current_line == '':
        bingo_cards += [current_card]
        current_card = []
        bingo_cards_tf += [current_card_tf]
        current_card_tf = []
        continue
    current_card_tf += [[False, False, False, False, False]]
    current_line = current_line.split(' ')
    temp = []
    for item in current_line:
        if item == '':
            continue
        temp += [int(item)]
    current_line = temp[:]
    current_card += [current_line]
bingo_cards += [current_card]
bingo_cards_tf += [current_card_tf]

# Cards made, now let's play
winning_card = []
winning_cards = []
winning_numbers = []
winning_number = -1
winning_card_idx = []
for number in bingo_numbers:
    number = int(number)
    for cardnum in range(len(bingo_cards)):
        id_number(number, bingo_cards[cardnum], bingo_cards_tf[cardnum])
        if check_winner(bingo_cards_tf[cardnum]) == True:
            winning_cards += [bingo_cards[cardnum][:]]
            winning_numbers += [number]
            winning_card_idx += [cardnum]
    winning_card_idx.reverse()
    for item in winning_card_idx:
        del bingo_cards[item]
        del bingo_cards_tf[item]
    winning_card_idx = []
    
    
part_1_score = calculate_score(winning_cards[0])
print('Part 1: score is ' + str(part_1_score * winning_numbers[0]))
part_2_score = calculate_score(winning_cards[-1])
print('Part 2: score is ' + str(part_2_score * winning_numbers[-1]))