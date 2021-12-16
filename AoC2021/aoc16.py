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

input_data = test_1
expanded_data = expand_data(input_data)
position = 0
version_sum = 0
def decode_packet(expanded_data, position=0):

    version_sum = 0
    original_position = position
    data_length = len(expanded_data)
    if position + 7 >= data_length:
        return(0, data_length)
    
    # Get type
    if position + 3 >= len(expanded_data):
            return (version_sum, len(expanded_data) - original_position)
    version_number = int(expanded_data[position:position+3], 2)
    version_sum += version_number
    position += 3
    # Get type
    if position + 3 > len(expanded_data):
        return (version_sum, len(expanded_data) - original_position)
    packet_type = int(expanded_data[position: position+3], 2)
    position += 3
    total_bits = 6
    if packet_type == 4:
        
        # For now, just throw away the values until you get to the next packet
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
        
    else:
        # I assume that I will have to parse this all out in part 2
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
        else:
            
            contained_packets = int(expanded_data[position:position+11], 2)
            position += 11
            for x in range(contained_packets):
                result = decode_packet(expanded_data, position)
                version_sum += result[0]
                position += result[1]
    bytes_moved = position - original_position
    return (version_sum, position - original_position)    

def decode_data(expanded_data):
    version_sum = 0
    position = 0
    data_length = len(expanded_data)
    while position < len(expanded_data):
        # Get version number
        
            #version_sum += decode(expanded_data[position:position+total_length])[0]
            result = decode_packet(expanded_data, position)
            version_sum += result[0]
            position += result[1]
            
            
    return (version_sum, position)

# Check first example

input_data = 'D2FE28'
expanded_data = expand_data(input_data)
result = decode_data(expanded_data)
print(result[0])

# Now cehck next example
input_data = '38006F45291200'
expanded_data = expand_data(input_data)
result = decode_data(expanded_data)
print(result[0])

input_data = 'EE00D40C823060'
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print(version_sum)
            
input_data = '8A004A801A8002F478'
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print(version_sum)

input_data = '620080001611562C8802118E34'
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print(version_sum)

input_data = 'C0015000016115A2E0802F182340'
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print(version_sum)

input_data = 'A0016C880162017C3686B18A3D4780'
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print(version_sum)

# Now look at our input
input_data = raw_input[0]
expanded_data = expand_data(input_data)
version_sum, _ = decode_data(expanded_data)
print('Part 1: sum of version numbers is ' + str(version_sum))