hex_in = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
base64_out = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def hex_to_base64(hex_string):
    value = hex_to_number(hex_string)
    digits = []
    while(value != 0):
        digits.append(value & 0b111111)
        value = value >> 6
    return ''.join(base64_char(x) for x in reversed(digits))

def hex_to_number(hex_string):
    value = 0
    for power, char in enumerate(hex_string[::-1]):
        value = value + hex_char_to_number(char) * 16 ** power
    return value

def hex_char_to_number(char):
    if char.isdigit():
        return int(char)
    else: 
        return ord(char.lower()) - ord('a') + 10

def base64_char(x):
    if x < 26:
        return chr(x + ord('A'))
    if x < 52:
        return chr(x + ord('a') - 26)
    if x < 62:
        return chr(x + ord('0') - 52)
    if x == 62:
        return '+'
    if x == 63:
        return '/'

if __name__ == '__main__':
    print(hex_to_base64(hex_in) == base64_out)
