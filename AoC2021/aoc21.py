from collections import Counter
import itertools
from functools import lru_cache
from typing import Tuple


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

def move(player, steps):
    new_position = (player[0] + steps) % 10
    if new_position == 0:
        new_position = 10
    return (new_position, player[1] + new_position)
    
player1 = (p1_pos, 0)
player2 = (p2_pos, 0)

while (player1[1] < 1000) and (player2[1] < 1000):
    # p1 first
    roll1 = (dice + 1) % 100 if (dice + 1) % 100 != 0 else 100
    roll2 = (dice + 2) % 100 if (dice + 2) % 100 != 0 else 100
    roll3 = (dice + 3) % 100 if (dice + 3) % 100 != 0 else 100
    dice += 3
    player1 = move(player1, roll1+roll2+roll3)

    rolls += 3
    if player1[1] >= 1000:
        continue
    roll1 = (dice + 1) % 100 if (dice + 1) % 100 != 0 else 100
    roll2 = (dice + 2) % 100 if (dice + 2) % 100 != 0 else 100
    roll3 = (dice + 3) % 100 if (dice + 3) % 100 != 0 else 100
    dice += 3
    player2 = move(player2, roll1+roll2+roll3)

    rolls += 3    
if player1[1] < player2[1]:
    losing_score = player1[1]
else:
    losing_score = player2[1]
print('Part 1: losing score * dice rolls is ' + str(losing_score * rolls))

dice_possibilities = Counter(map(sum, list(itertools.product((1,2,3), repeat=3))))

@lru_cache(maxsize=None)
def quantum_game(player1, player2) -> Tuple[int, int]:
    global dice_possibilities
    
    if player1[1] >= 21:
        return (1,0)
    if player2[1] >= 21:
        return (0,1)
    
    player1_wins_total = 0
    player2_wins_total = 0
    
    for roll, amount in dice_possibilities.items():
        new_player1 = move(player1, roll)
        player2_wins, player1_wins = quantum_game(player2, new_player1)
        
        player1_wins_total += player1_wins * amount
        player2_wins_total += player2_wins * amount
        
    return(player1_wins_total, player2_wins_total)
        
  

p1_pos = int(raw_input[0].split(': ')[1])
p2_pos = int(raw_input[1].split(': ')[1])
player1 = (p1_pos, 0)
player2 = (p2_pos, 0)
victories = quantum_game(player1, player2)
print('Part 2: Maximum wins is ' + str(max(victories)))

