f = open('aoc17.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()

def get_bounds(rule):
    # example: target area: x=20..30, y=-10..-5
    coordinate_text = rule.split(': ')[1]
    x_text = coordinate_text.split(', ')[0]
    y_text = coordinate_text.split(', ')[1]
    x_min = int(x_text.split('=')[1].split('..')[0])
    x_max = int(x_text.split('=')[1].split('..')[1])
    y_min = int(y_text.split('=')[1].split('..')[0])
    y_max = int(y_text.split('=')[1].split('..')[1])
    return [(x_min, x_max),(y_min, y_max)]

example_rule = 'target area: x=20..30, y=-10..-5'
target_bounds = get_bounds(example_rule)

#target_bounds = get_bounds(raw_input[0])
good_x = {}
good_y = {} 
# Start by finding good X values that fall within the bounds
starting_x = 0
x_min = target_bounds[0][0]
x_max = target_bounds[0][1]
overshoot = False
for starting_x in range(x_max + 1):
    in_target = False
    x_vel = starting_x

    steps = 0
    x_pos = 0
    while x_vel != 0:
        steps += 1
        x_pos += x_vel
        x_vel -= 1 if x_vel > 0 else 0
        if (x_pos >= x_min) and (x_pos <= x_max):
            in_target = True
            if starting_x not in good_x:
                good_x[starting_x] = [steps]
            else:
                good_x[starting_x] += [steps]
        elif x_pos > x_max:
            if in_target == False:
                overshoot = True
            break
        if x_vel == 0:
            if starting_x in good_x:
                good_x[starting_x] += [999999999999999999999999]
    starting_x += 1 

# Now we have good X values, time to use that to find good Y values
for x in good_x:
    valid_steps = good_x[x]
    overshoot = False
    min_step = min(valid_steps)
    max_step = max(valid_steps)
    y_min = target_bounds[1][0]
    y_max = target_bounds[1][1]    
    starting_y = y_min #based on rules, this is the 'lowest' velocity you can have and make it in the Y target range
    temp1 = 0
    for counter in range(y_min, 3*(abs(y_max))):
        in_target = False
        y_vel = starting_y

        steps = 0
        y_pos = 0
        if (starting_y > (5*abs(y_min))):
            overshoot = True
            continue
        if max_step != 999999999999999999999999:
            while steps <= max_step:
                steps += 1
                y_pos += y_vel
                y_vel -= 1
                if (y_pos >= y_min) and (y_pos <= y_max) and steps >= min_step:
                    in_target = True
                    if (x, starting_y) not in good_y:
                        good_y[(x, starting_y)] = [steps]
                    else:
                        good_y[(x, starting_y)] += [steps]
        else:
            while y_pos > y_min:
                steps += 1
                y_pos += y_vel
                y_vel -= 1
                if (y_pos >= y_min) and (y_pos <= y_max) and steps >= min_step:
                    in_target = True
                    if (x, starting_y) not in good_y:
                        good_y[(x, starting_y)] = [steps]
                    else:
                        good_y[(x, starting_y)] += [steps] 

        starting_y += 1

# Now that we have found good velocities, get the highest initial Y velocity
# Determine if we have any times that x falls to 0
calculation = False
for item in good_x:
    if 999999999999999999999999 in good_x[item]:
        calculation = True
if calculation == True:
    # velocity needs to be the same as y_min at 0, so start from there
    y_pos = 0
    y_vel = abs(y_min)
    while y_vel > 0:
        y_vel -= 1
        y_pos += y_vel
        
print('Part 1: highest y reached is ' + str(y_pos))


# 1653 too low

        