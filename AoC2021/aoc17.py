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

target_bounds = get_bounds(raw_input[0])
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
                good_x[starting_x] += [99999]
    starting_x += 1 


# Find good y values that fall within the bounds.
y_min = target_bounds[1][0]
y_max = target_bounds[1][1]   
for y_initial in range(y_min, 3 * abs(y_min)):
    steps = 0
    y_vel = y_initial
    y_pos = 0
    while y_pos > y_min:
        steps += 1
        y_pos += y_vel
        y_vel -= 1
        if (y_pos <= y_max) and (y_pos >= y_min):
            if y_initial not in good_y:
                good_y[y_initial] = [steps]
            else:
                good_y[y_initial] += [steps]
                
# Now see where good X and Y line up on compatible steps
good_points = {}
for y_coord in good_y:
    good_steps = good_y[y_coord]
    for y_step in good_steps:
        for x_coord in good_x:
            min_step = min(good_x[x_coord])
            max_step = max(good_x[x_coord])
            
            if y_step in range(min_step, max_step + 1):
                good_points[(x_coord, y_coord)] = 1

# Now that we have found good velocities, get the highest initial Y velocity
# Determine if we have any times that x falls to 0, as at that point we can shoot a theoretical maximum y velocity
calculation = False
for item in good_x:
    if 99999 in good_x[item]:
        calculation = True
if calculation == True:
    # velocity needs to be the same as y_min at 0, so start from there
    y_pos = 0
    y_vel = abs(y_min)
    while y_vel > 0:
        y_vel -= 1
        y_pos += y_vel
# NOTE: if there aren't any good X points that fall to a x_vel of 0 we are hosed.  Need to actually calculate the long way of looping through all of the good points.
        
print('Part 1: highest y reached: ' + str(y_pos))
print('Part 2: distinct inital velocity points: ' + str(len(good_points)))
        