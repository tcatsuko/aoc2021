f = open('aoc16.txt','rt')
raw_input = []
for line in f:
    raw_input += [line[:-1]]
f.close()
test_1 = 'D2FE28'

# Hex dictionary
hex_dict = {'0':'0000', '1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','A':'1010','B':'1011','C':'1100','D':'1101','E':'1110','F':'1111'}


def expand_data(input_data):
    global hex_dict
    expanded_data = ''
    for letter in input_data:
        expanded_data += hex_dict[letter]
    return expanded_data

def decode_packet(expanded_data, position=0):
    version_sum = 0
    original_position = position
    data_length = len(expanded_data)
    if position + 7 >= data_length:
        return(0, data_length, [])
    if position + 3 >= len(expanded_data):
            return (version_sum, len(expanded_data) - original_position, [])
    version_number = int(expanded_data[position:position+3], 2)
    version_sum += version_number
    position += 3
    if position + 3 > len(expanded_data):
        return (version_sum, len(expanded_data) - original_position)
    packet_type = int(expanded_data[position: position+3], 2)
    position += 3
    total_bits = 6
    if packet_type == 4:
        data_bits = expanded_data[position: position + 5]
        number = ''
        while data_bits[0] == '1':
            total_bits += 5
            number += data_bits[1:]
            position += 5
            data_bits = expanded_data[position: position + 5]
        # This is the final grouping
        number += data_bits[1:]
        number = int(number, 2)
        position += 5
        num_to_return = number
    else:
        num_to_return = 0
        numbers = []
        length_number = expanded_data[position]
        position += 1
        total_bits += 1
        if length_number == '0':
            length_binary = expanded_data[position:position + 15]
            total_length = int(expanded_data[position:position+15], 2)
            position += 15
            total_bits += 15
            result = decode_data(expanded_data[position:position+total_length])
            version_sum += result[0]
            position += result[1]
            numbers += result[2]
        else:
            contained_packets = int(expanded_data[position:position+11], 2)
            position += 11
            for x in range(contained_packets):
                result = decode_packet(expanded_data, position)
                version_sum += result[0]
                position += result[1]
                numbers += [result[2]]
        if packet_type == 0:
            my_sum = 0
            for item in numbers:
                my_sum += item
            num_to_return = my_sum
        elif packet_type == 1:
            product = 1
            for item in numbers:
                product *= item
            num_to_return = product
        elif packet_type == 2:
            num_to_return = min(numbers)
        elif packet_type == 3:
            num_to_return = max(numbers)
        elif packet_type == 5:
            if numbers[0] > numbers[1]:
                num_to_return = 1
            else:
                num_to_return = 0
        elif packet_type == 6:
            if numbers[0] < numbers[1]:
                num_to_return = 1
            else:
                num_to_return = 0
        elif packet_type == 7:
            if numbers[0] == numbers[1]:
                num_to_return = 1
            else:
                num_to_return = 0
    bytes_moved = position - original_position
    return (version_sum, position - original_position, num_to_return)    

def decode_data(expanded_data):
    numbers = []
    version_sum = 0
    position = 0
    data_length = len(expanded_data)
    while position < len(expanded_data):
        result = decode_packet(expanded_data, position)
        version_sum += result[0]
        position += result[1]
        numbers += [result[2]]
          
    return (version_sum, position, numbers)


# Now look at our input
input_data = raw_input[0]
expanded_data = expand_data(input_data)
result = decode_data(expanded_data)
version_sum = result[0]
print('Part 1: sum of version numbers is ' + str(version_sum))
print('Part 2: resulting output is ' + str(result[2][0]))

