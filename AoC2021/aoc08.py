f = open('aoc08.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]

# Part 1 - count 1, 4, 7, 8
unique_counter = 0
for line in raw_input:
    outputs = line.split(' | ')[1].split(' ')
    for item in outputs:
        if (len(item) == 2) or (len(item)==4) or (len(item)==3) or (len(item)==7):
            unique_counter += 1
print('Part 1: 1, 4, 7, and 8 appear ' + str(unique_counter) + ' times.')


def sort_string(signal):
    temp = []
    for item in signal:
        temp += [item]
    temp.sort()
    return ''.join(temp)

def decode(signals):
    digits = {}
    # build up initial dictionary
    for item in signals:
        digits[item] = ''
    # build sets
    zero = set()
    one = set()
    two = set()
    three = set()
    four = set()
    five = set()
    six = set()
    seven = set()
    eight = set()
    nine = set()
    
    # Now time for some logic!
    # Create sets for the digits we know
    
    for item in signals:
        if len(item) == 2:
            digits[item] = '1'
            for letter in item:
                one.add(letter)
        elif len(item) == 4:
            digits[item] = '4'
            for letter in item:
                four.add(letter)
        elif len(item) == 3:
            digits[item] = '7'
            for letter in item:
                seven.add(letter)
        elif len(item) == 7:
            digits[item] = '8'
            for letter in item:
                eight.add(letter)

    # digits found: 1, 4, 7, 8
    # Find nine using 4 and 7
    mask_set = four.union(seven)
    for item in signals:
        if len(item) == 6:
            test_set = set()
            for letter in item:
                test_set.add(letter)
            if mask_set.issubset(test_set):
                # We found nine
                digits[item] = '9'
                nine = test_set
    
    # digits found: 1, 4, 7, 8, 9
    # Find two, three and five using nine and one
    for item in signals:
        if len(item) == 5:
            test_set = set()
            for letter in item:
                test_set.add(letter)
            if test_set.issubset(nine):
                # can be 3 or 5
                if one.issubset(test_set):
                    # it's 3
                    three = test_set
                    digits[item] = '3'
                else:
                    # it's 5
                    five = test_set
                    digits[item] = '5'
            else:
                # its 2
                two = test_set
                digits[item] = '2'
    
    # digits found: 1, 2, 3, 4, 5, 7, 8, 9
    # Find zero and six using 5
    for item in signals:
        if len(item) == 6:
            test_set = set()
            for letter in item:
                test_set.add(letter)
            if test_set == nine:
                continue
            if five.issubset(test_set):
                # it's 6
                six = test_set
                digits[item] = '6'
            else:
                # it's 0
                zero = test_set
                digits[item] = '0'
    return digits
    

# Part 2: time to decode!
output_sum = 0
for line in raw_input:
    test_signal = line.split(' | ')[0].split(' ')
    output_signal = line.split(' | ')[1].split(' ')
    
    # Sort the letters to make things a little easier
    sorted_signal = []
    for item in test_signal:
        sorted_signal += [sort_string(item)]
    # Pass the sorted string to the decoder, receive a dictionary of decoded digits
    digits = decode(sorted_signal)
    
    # Sort the letters of the output
    sorted_signal = []
    for item in output_signal:
        sorted_signal += [sort_string(item)]
    
    # Translate the output numbers
    output_digit_string = ''
    for item in sorted_signal:
        output_digit_string += digits[item]
    # Add this to the output sum
    output_sum += int(output_digit_string)
    
print('Part 2: the sum of the output values is ' + str(output_sum))
