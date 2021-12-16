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


def decode(expanded_data):
    version_sum = 0
    position = 0
    while position < len(expanded_data):
        # Get version number
        if position + 3 >= len(expanded_data):
            return (version_sum, position)
        version_number = int(expanded_data[position:position+3], 2)
        version_sum += version_number
        position += 3
        # Get type
        if position + 3 > len(expanded_data):
            return (version_sum, position)
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
        elif packet_type == 0 and version_number == 0:
            # Padded zeroes
            return (version_sum, position)
            
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
                
            else:
                
                contained_packets = int(expanded_data[position:position+11], 2)
                for x in range(contained_packets):
                    
            version_sum += decode(expanded_data[position:position+total_length])[0]
            position += total_length
            
            
    return (version_sum, position)

# Check first example

input_data = test_1
expanded_data = expand_data(input_data)

result = decode(expanded_data)
print(result[0])

# Now cehck next example
input_data = '38006F45291200'
expanded_data = expand_data(input_data)
version_sum, _ = decode(expanded_data)
print(version_sum)

input_data = 'EE00D40C823060'
expanded_data = expand_data(input_data)
version_sum, _ = decode(expanded_data)
print(version_sum)
            
    