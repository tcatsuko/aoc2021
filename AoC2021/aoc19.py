import math
f = open('test_aoc19.txt','rt')
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
        fingerprints = set()
        for other_beacon in other_beacons:
            current_fingerprint = get_fingerprint(beacon[0], other_beacon[0])
            fingerprints.add((current_fingerprint[0:3]))
        scanner[idx] = (beacon[0], fingerprints, current_fingerprint[3])

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
        beacon_pos = beacon[0]
        beacon_fingerprint = beacon[1]
        beacon_offset = beacon[2]
        new_beacon_pos = []
        new_beacon_offset = []
        new_beacon_offset += [beacon_offset[x_trans[0]] * x_trans[1]]
        new_beacon_offset += [beacon_offset[y_trans[0]] * y_trans[1]]
        new_beacon_offset += [beacon_offset[z_trans[0]] * z_trans[1]]        
        new_beacon_pos += [beacon_pos[x_trans[0]] * x_trans[1]]
        new_beacon_pos += [beacon_pos[y_trans[0]] * y_trans[1]]
        new_beacon_pos += [beacon_pos[z_trans[0]] * z_trans[1]]
        if beacon_pos == beacon_pair[1][0]:
            offset_pos = new_beacon_pos
        print()
        translated_scanner += [[new_beacon_pos, beacon_fingerprint, new_beacon_offset]]
    offset_x = reference_pos[0]-offset_pos[0]
    offset_y = reference_pos[1] - offset_pos[1]
    offset_z = reference_pos[2] - offset_pos[2]
    for counter in range(len(translated_scanner)):
        translated_scanner[counter][0][0] += offset_x
        translated_scanner[counter][0][1] += offset_y
        translated_scanner[counter][0][2] += offset_z
        beacon_tuple = (translated_scanner[counter][0][0], translated_scanner[counter][0][1], translated_scanner[counter][0][2])
        beacon_positions.add(beacon_tuple)
    print()
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
                        test1 = beacon[1].intersection(other_beacon[1])
                        if len(beacon[1].intersection(other_beacon[1]))>= 4:
                            matched_points += [(other_beacon[0], beacon[0])]
                            matched_beacons += [(other_beacon, beacon)]
                        if len(matched_points) >= 5:
                            print('Good Overlap')
                            # Found a match!
                            # will need to rotate later, for now just move them up
                            # Get the offset matrix
                            
                            found_rotation = False
                            for pair in matched_beacons:
                                reference_offset = pair[0][2]
                                coordinate = pair[1][2]
                                if (abs(reference_offset[0]) == abs(reference_offset[1])) or (abs(reference_offset[0]) == abs(reference_offset[2])) or (abs(reference_offset[1]) == abs(reference_offset[2])):
                                    continue
                                if (reference_offset[0] == 0) or (reference_offset[1] == 0) or (reference_offset[2] == 0):
                                    continue
                                # Find x transformation
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
                            # Check first orientation (1)
                            #if check_offsets(matched_points[:3]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 0)
                                #add_to_found(matched_points, current_unmatched_rotated, current_unmatched)
                                #print('Matched original orientation')
                                #match_scanner = True
                                #break
                            ## Rotate 90 around x (2)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_3 = rotate(point_3, 'x', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90')
                                #match_scanner = True
                                #break
                            ## Rotate 90 around y (3)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_3 = rotate(point_3, 'y', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'y', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched y 90')
                                #match_scanner = True
                                #break
                            ## Rotate 90 around z (4)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'z', 90)
                            #point_2 = rotate(point_2, 'z', 90)
                            #point_3 = rotate(point_3, 'z', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'z', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched z 90')
                                #match_scanner = True
                                #break                            
                            ## XX (5)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_3 = rotate(point_3, 'x', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 180')
                                #match_scanner = True
                                #break
                            ## XY (6)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'y', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, y 90')
                                #match_scanner = True
                                #break                                 
                            ## XZ (7))
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'z', 90)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'z', 90)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'z', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'z', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, z 90')
                                #match_scanner = True
                                #break     
                            ## yx (8)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_3 = rotate(point_3, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'y', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'x', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched y 90, x 90')
                                #match_scanner = True
                                #break  
                            ## YY (9)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'y', 180)
                            #point_2 = rotate(point_2, 'y', 180)
                            #point_3 = rotate(point_3, 'y', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'y', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched y 180')
                                #match_scanner = True
                                #break   
                            ## ZY (10)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'z', 90)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_2 = rotate(point_2, 'z', 90)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_3 = rotate(point_3, 'z', 90)
                            #point_3 = rotate(point_3, 'y', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'z', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched z 90, y 90')
                                #match_scanner = True
                                #break   
                            ## ZZ (11)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'z', 180)
                            #point_2 = rotate(point_2, 'z', 180)
                            #point_3 = rotate(point_3, 'z', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'z', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched z 180')
                                #match_scanner = True
                                #break 
                            ## XXX (2)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 270)
                            #point_2 = rotate(point_2, 'x', 270)
                            #point_3 = rotate(point_3, 'x', 270)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 270)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 270')
                                #match_scanner = True
                                #break     
                            ## XXY (13)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #point_3 = rotate(point_3, 'y', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 180)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 180, y 90')
                                #match_scanner = True
                                #break      
                            ## XXZ (14)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_1 = rotate(point_1, 'z', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_2 = rotate(point_2, 'z', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #point_3 = rotate(point_3, 'z', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 180)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'z', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 180, z 90')
                                #match_scanner = True
                                #break 
                            ## ZXX (15)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'z', 90)
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_2 = rotate(point_2, 'z', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_3 = rotate(point_3, 'z', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'z', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'x', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched z 90, x 180')
                                #match_scanner = True
                                #break   
                            ## XYY (16)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'y', 180)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'y', 180)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'y', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, y 180')
                                #match_scanner = True
                                #break   
                            ## XZZ (17)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'z', 180)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'z', 180)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'z', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'z', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, z 180')
                                #match_scanner = True
                                #break      
                            ## YXX (18)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_3 = rotate(point_3, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'y', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'x', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched y 90, x 180')
                                #match_scanner = True
                                #break     
                            ## YYY (19)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'y', 270)
                            #point_2 = rotate(point_2, 'y', 270)
                            #point_3 = rotate(point_3, 'y', 270)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'y', 270)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched y 270')
                                #match_scanner = True
                                #break 
                            ## ZZZ (20)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'z', 270)
                            #point_2 = rotate(point_2, 'z', 270)
                            #point_3 = rotate(point_3, 'z', 270)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'z', 270)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched z 270')
                                #match_scanner = True
                                #break  
                            ## XXXY (21)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 270)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 270)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 270)
                            #point_3 = rotate(point_3, 'y', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 270)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 270, y 90')
                                #match_scanner = True
                                #break    
                            ## XXYX (22)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #point_3 = rotate(point_3, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 90)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 180)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'x', 90)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 180, y 90, x 90')
                                #match_scanner = True
                                #break  
                            ## XYXX (23)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'y', 90)
                            #point_1 = rotate(point_1, 'x', 180)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'y', 90)
                            #point_2 = rotate(point_2, 'x', 180)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'y', 90)
                            #point_3 = rotate(point_3, 'x', 180)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'x', 180)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, y 90, x 180')
                                #match_scanner = True
                                #break  
                            ## XYYY (24)
                            #point_1 = matched_points[0][1]
                            #point_2 = matched_points[1][1]
                            #point_3 = matched_points[2][1]
                            #point_1 = rotate(point_1, 'x', 90)
                            #point_1 = rotate(point_1, 'y', 270)
                            #point_2 = rotate(point_2, 'x', 90)
                            #point_2 = rotate(point_2, 'y', 270)
                            #point_3 = rotate(point_3, 'x', 90)
                            #point_3 = rotate(point_3, 'y', 270)
                            #if check_offsets([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]]):
                                #current_unmatched_rotated = rotate_scanner(current_unmatched, 'x', 90)
                                #current_unmatched_rotated = rotate_scanner(current_unmatched_rotated, 'y', 270)
                                #add_to_found([[matched_points[0][0], point_1],[matched_points[1][0],point_2],[matched_points[2][0],point_3]], current_unmatched_rotated, current_unmatched)
                                #print('Matched x 90, y 270')
                                #match_scanner = True
                                #break                                
                            if current_unmatched in scanners_raw:
                                test1 = 0
                                #print('Failed to find orientation somehow')
                        if match_scanner == True:
                            break
            idx += 1
print('Part 1: there are ' + str(len(beacon_positions)) + ' beacons')

        