import math
f = open('aoc19.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
idx = 0
scanners_raw = []
current_scanner = []

while idx < len(raw_input):
    
    if raw_input[idx] == '':
        idx += 1
        continue
    elif raw_input[idx][0:2] == '--':
        # This is a new scanner
        if current_scanner != []:
            scanners_raw +=[current_scanner]
        current_scanner = []
        idx += 1
        continue
    point = [int(x) for x in raw_input[idx].split(',')]
    point = (point[0], point[1], point[2])
    current_scanner += [[point]]
    idx += 1
scanners_raw += [current_scanner]

def get_fingerprint(point1, point2):
    distance = math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0]) + (point1[1]-point2[1])*(point1[1]-point2[1]) + (point1[2]-point2[2])*(point1[2]-point2[2]))
    min_offset = min([abs(point1[0]-point2[0]),abs(point1[1]-point2[1]),abs(point1[2]-point2[2])])
    max_offset = max([abs(point1[0]-point2[0]),abs(point1[1]-point2[1]),abs(point1[2]-point2[2])])
    offset = (point1[0]-point2[0], point1[1]-point2[1], point1[2]-point2[2])
    return(distance, min_offset, max_offset, offset)

def rotate(vector, axis, degrees):
    cos_deg = int(math.cos(math.radians(degrees)))
    sin_deg = int(math.sin(math.radians(degrees)))
    
    new_vector = []
    if axis == 'x':
        new_vector += [vector[0]]
        new_vector += [vector[1] * cos_deg - vector[2] * sin_deg]
        new_vector += [vector[1] * sin_deg + vector[2] * cos_deg]
    elif axis == 'y':
        new_vector += [vector[0] * cos_deg + vector[2] * sin_deg]
        new_vector += [vector[1]]
        new_vector += [(-1 * vector[0] * sin_deg) + vector[2] * cos_deg]
    elif axis == 'z':
        new_vector += [vector[0] * cos_deg - vector[1] * sin_deg]
        new_vector += [vector[0] * sin_deg + vector[1] * cos_deg]
        new_vector += [vector[2]]
    return new_vector
    
# Fingerprint each beacon seen by a scanner
for scanner in scanners_raw:
    for idx, beacon in enumerate(scanner):
        other_beacons = scanner[:]
        other_beacons.remove(beacon)
        fingerprints = []
        offsets = []
        for other_beacon in other_beacons:
            current_fingerprint = get_fingerprint(beacon[0], other_beacon[0])
            fingerprints += [current_fingerprint[0:3]]
            offsets += [current_fingerprint[3]]
        scanner[idx] = (beacon[0], fingerprints, offsets)

# Start to match points
found_scanners = []
found_scanners += [scanners_raw[0]]
beacon_positions = set()
scanner_positions = []
scanner_positions += [(0,0,0)]
for beacon in found_scanners[0]:
    beacon_positions.add(beacon[0])
del scanners_raw[0]

def check_offsets(matched_points):
    offset_x1 = matched_points[0][0][0] - matched_points[0][1][0]
    offset_y1 = matched_points[0][0][1] - matched_points[0][1][1]
    offset_z1 = matched_points[0][0][2] - matched_points[0][1][2]
    
    offset_x2 = matched_points[1][0][0] - matched_points[1][1][0]
    offset_y2 = matched_points[1][0][1] - matched_points[1][1][1]
    offset_z2 = matched_points[1][0][2] - matched_points[1][1][2]
    
    offset_x3 = matched_points[2][0][0] - matched_points[2][1][0]
    offset_y3 = matched_points[2][0][1] - matched_points[2][1][1]
    offset_z3 = matched_points[2][0][2] - matched_points[2][1][2]                
    
    if (offset_x1 == offset_x2 == offset_x3) and (offset_y1 == offset_y2 == offset_y3) and (offset_z1 == offset_z2 == offset_z3):
        return True
    return False

def add_to_found(matched_points, current_unmatched, current_unmatched_orig):
    global scanners_raw
    global scanner_positions
    global beacon_positions
    global found_scanners
    
    offset_x = matched_points[0][0][0] - matched_points[0][1][0]
    offset_y = matched_points[0][0][1] - matched_points[0][1][1]
    offset_z = matched_points[0][0][2] - matched_points[0][1][2]                    
    # lined up
    scanner_positions += [(offset_x, offset_y, offset_z)]
    adjusted_matched = []
    for beacon in current_unmatched:
        new_beacon = []
        x = beacon[0][0] + offset_x
        y = beacon[0][1] + offset_y
        z = beacon[0][2] + offset_z
        new_beacon_point = (x, y, z)
        new_beacon_fingerprint = set()
        for item in beacon[1]:
            new_beacon_fingerprint.add(item)
        new_beacon = [new_beacon_point, new_beacon_fingerprint]
        
        adjusted_matched += [new_beacon]
        beacon_positions.add((x, y, z))
    found_scanners += [adjusted_matched]
    scanners_raw.remove(current_unmatched_orig)
    
def rotate_scanner(scanner_orig, axis, degrees):
    rotated_scanner = []
    for beacon in scanner_orig:
        new_beacon_pos = rotate(beacon[0], axis, degrees)
        new_beacon_fingerprint = set()
        for item in beacon[1]:
            new_beacon_fingerprint.add(item)
        rotated_scanner += [[new_beacon_pos, new_beacon_fingerprint]]
    return rotated_scanner
found_scanner_indices = [0]

def translate_and_add(scanner_orig, beacon_pair, x_trans, y_trans, z_trans):
    global scanners_raw
    global scanner_positions
    global beacon_positions
    global found_scanners
    
    translated_scanner = []
    good_fingerprint = beacon_pair[0][1]
    reference_pos = beacon_pair[0][0]
    for beacon in scanner_orig:
        calculate_offset = False
        beacon_pos = beacon[0]
        beacon_fingerprint = beacon[1]
        beacon_offset = beacon[2]
        new_beacon_pos = []
        new_beacon_offset = []
        good_pair_pos = (beacon_pair[1][0][0], beacon_pair[1][0][1], beacon_pair[1][0][2])
        current_beacon_pos = (beacon[0][0], beacon[0][1], beacon[0][2])
        if good_pair_pos == current_beacon_pos:
            calculate_offset = True
        for item in beacon_offset:
            new_offset_x = item[x_trans[0]] * x_trans[1]
            new_offset_y = item[y_trans[0]] * y_trans[1]
            new_offset_z = item[z_trans[0]] * z_trans[1]
            new_beacon_offset += [(new_offset_x, new_offset_y, new_offset_z)]
    
        new_beacon_pos += [beacon_pos[x_trans[0]] * x_trans[1]]
        new_beacon_pos += [beacon_pos[y_trans[0]] * y_trans[1]]
        new_beacon_pos += [beacon_pos[z_trans[0]] * z_trans[1]]
        new_beacon_pos = (new_beacon_pos[0], new_beacon_pos[1], new_beacon_pos[2])
        if calculate_offset == True:
            good_position = beacon_pair[0][0]
            offset_x = good_position[0] - new_beacon_pos[0]
            offset_y = good_position[1] - new_beacon_pos[1]
            offset_z = good_position[2] - new_beacon_pos[2]

        translated_scanner += [[new_beacon_pos, beacon_fingerprint, new_beacon_offset]]

    # Get offset
    matched_beacon_pos_old = beacon_pair[1][1]
    
    for counter in range(len(translated_scanner)):

        translated_scanner[counter][0] = (translated_scanner[counter][0][0] + offset_x, translated_scanner[counter][0][1] + offset_y, translated_scanner[counter][0][2] + offset_z)
        beacon_tuple = (translated_scanner[counter][0][0], translated_scanner[counter][0][1], translated_scanner[counter][0][2])
        beacon_positions.add(beacon_tuple)
    scanner_positions += [(offset_x, offset_y, offset_z)]
    found_scanners += [translated_scanner]
    scanners_raw.remove(scanner_orig)
        # get x coordinate:
    
while scanners_raw != []:
    
    while len(scanners_raw) > 0:
        idx = 0
        while idx < len(scanners_raw):
            current_unmatched = scanners_raw[idx]
            
            matched_scanner = []
            match_scanner = False
            for scanner in found_scanners:
                matched_points = []
                matched_beacons = []
                for beacon in current_unmatched:
                    if match_scanner == True:
                        break
                    for other_beacon in scanner:
                        #if beacon[1] == other_beacon[1]:
                        test1 = set(beacon[1]).intersection(set(other_beacon[1]))
                        if len(set(beacon[1]).intersection(set(other_beacon[1])))>= 4:
                            matched_points += [(other_beacon[0], beacon[0])]
                            matched_beacons += [(other_beacon, beacon)]
                        if len(matched_points) >= 5:
                            # Found a match!
                            # will need to rotate later, for now just move them up
                            # Get the offset matrix
                            
                            found_rotation = False
                            found_good_match = False
                            for pair in matched_beacons:
                                # Find a fingerprint that is the same
                                known_beacon = pair[0]
                                unknown_beacon = pair[1]
                                if found_good_match == True:
                                    break
                                for idx, fingerprint in enumerate(known_beacon[1]):
                                    if found_good_match == True:
                                        break
                                    if fingerprint in unknown_beacon[1]:
                                        unknown_index = unknown_beacon[1].index(fingerprint)
                                        reference_offset = unknown_beacon[2][unknown_index]
                                        if (abs(reference_offset[0]) == abs(reference_offset[1])) or (abs(reference_offset[0]) == abs(reference_offset[2])) or (abs(reference_offset[1]) == abs(reference_offset[2])):
                                            continue
                                        if (reference_offset[0] == 0) or (reference_offset[1] == 0) or (reference_offset[2] == 0):
                                            continue
                                        good_offset = reference_offset
                                        coordinate = known_beacon[2][idx]
                                        found_good_match = True

                                reference_offset = good_offset
                                

                                reference_offset = good_offset
                                found_rotation = True
                                good_x = reference_offset[0]
                                good_y = reference_offset[1]
                                good_z = reference_offset[2]
                                
                                if coordinate[0] == good_x:
                                    x_trans = (0,1)
                                elif coordinate[0] == -1 * good_x:
                                    x_trans = (0,-1)
                                elif coordinate[0] == good_y:
                                    x_trans = (1,1)
                                elif coordinate[0] == -1 * good_y:
                                    x_trans = (1,-1)
                                elif coordinate[0] == good_z:
                                    x_trans = (2,1)
                                elif coordinate[0] == -1 * good_z:
                                    x_trans = (2,-1)
                                    
                                if coordinate[1] == good_x:
                                    y_trans = (0,1)
                                elif coordinate[1] == -1 * good_x:
                                    y_trans = (0,-1)
                                elif coordinate[1] == good_y:
                                    y_trans = (1,1)
                                elif coordinate[1] == -1 * good_y:
                                    y_trans = (1,-1)
                                elif coordinate[1] == good_z:
                                    y_trans = (2,1)
                                elif coordinate[1] == -1 * good_z:
                                    y_trans = (2,-1)
                                if coordinate[2] == good_x:
                                    z_trans = (0,1)
                                elif coordinate[2] == -1 * good_x:
                                    z_trans = (0,-1)
                                elif coordinate[2] == good_y:
                                    z_trans = (1,1)
                                elif coordinate[2] == -1 * good_y:
                                    z_trans = (1,-1)
                                elif coordinate[2] == good_z:
                                    z_trans = (2,1)
                                elif coordinate[2] == -1 * good_z:
                                    z_trans = (2,-1)                                   
                                break
                            translate_and_add(current_unmatched, matched_beacons[0], x_trans, y_trans, z_trans)
                           
                            match_scanner = True
                            
                            if current_unmatched in scanners_raw:
                                #test1 = 0
                                print('Failed to find orientation somehow')
                        if match_scanner == True:
                            break
            idx += 1
print('Part 1: there are ' + str(len(beacon_positions)) + ' beacons')

# Part 2
# Glad I was already saving the location of scanners
max_manhattan = 0
for idx, scanner in enumerate(scanner_positions):
    if idx == len(scanner_positions) - 1:
        continue
    current_scanner = scanner_positions[idx]
    remaining_scanners = scanner_positions[idx + 1:]
    for other_scanner in remaining_scanners:
        manhattan = abs(current_scanner[0] - other_scanner[0]) + abs(current_scanner[1] - other_scanner[1]) + abs(current_scanner[2] - other_scanner[2])
        if manhattan > max_manhattan:
            max_manhattan = manhattan
print('Part 2: the largest manhattan distance between any two scanners is ' + str(max_manhattan))
   