f = open('aoc21.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
p1_pos = int(raw_input[0].split(': ')[1])
p2_pos = int(raw_input[1].split(': ')[1])
p1_score = 0
p2_score = 0
dice = 0
rolls = 0
while (p1_score < 1000) and (p2_score < 1000):
    # p1 first
    roll1 = (dice + 1) % 100 if (dice + 1) % 100 != 0 else 100
    roll2 = (dice + 2) % 100 if (dice + 2) % 100 != 0 else 100
    roll3 = (dice + 3) % 100 if (dice + 3) % 100 != 0 else 100
    dice += 3
    p1_pos += ((roll1 + roll2 + roll3) % 10) 
    if p1_pos % 10 == 0:
        p1_pos = 10
    else:
        p1_pos = p1_pos % 10
    p1_score += p1_pos
    rolls += 3
    if p1_score >= 1000:
        continue
    roll1 = (dice + 1) % 100 if (dice + 1) % 100 != 0 else 100
    roll2 = (dice + 2) % 100 if (dice + 2) % 100 != 0 else 100
    roll3 = (dice + 3) % 100 if (dice + 3) % 100 != 0 else 100
    dice += 3
    p2_pos += (roll1 + roll2 + roll3)
    if p2_pos % 10 == 0:
        p2_pos = 10
    else:
        p2_pos = p2_pos % 10
    p2_score += p2_pos    
    rolls += 3    
if p1_score < p2_score:
    losing_score = p1_score
else:
    losing_score = p2_score
print('Part 1: losing score * dice rolls is ' + str(losing_score * rolls))
