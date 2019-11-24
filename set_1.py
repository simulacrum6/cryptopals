def hex_to_base64(hex_string):
    value = hex_to_number(hex_string)
    digits = []
    while value != 0:
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

def xor_hex(hex_string_a, hex_string_b):
    bits = xor_bits(hex_to_number(hex_string_a), hex_to_number(hex_string_b))
    return bits_to_hex(bits)

def xor_bits(a, b):
    value = 0
    power = 0
    mask = 0b1
    while a != 0 or b != 0:
        value = value + xor(a & mask, b & mask) * 2 ** power
        power = power + 1
        a = a >> 1
        b = b >> 1
    return value

def xor(a, b):
    return int(a + b == 1)

def bits_to_hex(a):
    digits = []
    while a != 0:
        digits.append(a & 0b1111)
        a = a >> 4
    return ''.join(number_to_hex(digit) for digit in reversed(digits))

def number_to_hex(x):
    if x < 10:
        return chr(x + ord('0'))
    else:
        return chr(x + ord('a') - 10)

def is_passed(passed):
    if passed:
        return 'passed'
    else:
        return 'failed'

if __name__ == '__main__':
    print('cryptopals.com challenges')
    print('=========================')

    # set 1-1
    hex_in = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    base64_out = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    base64_out_actual = hex_to_base64(hex_in)
    print(f'Set 1-1: Base64 ({is_passed(base64_out == base64_out_actual)})')
    print(f'In: \t{hex_in}')
    print(f'Out:\t{base64_out} (expected)\n\t{base64_out_actual} (actual)')
    print(f'Passed: {base64_out == base64_out_actual}')
    print('-------')

    # set 1-2
    xor_in_1 = '1c0111001f010100061a024b53535009181c'
    xor_in_2 = '686974207468652062756c6c277320657965'
    xor_out = '746865206b696420646f6e277420706c6179'
    xor_out_actual = xor_hex(xor_in_1, xor_in_2)
    print(f'Set 1-2: XOR ({is_passed(xor_out == xor_out_actual)})')
    print(f'In: \t{xor_in_1}\n\t{xor_in_2}')
    print(f'Out:\t{xor_out} (expected)\n\t{xor_out_actual} (actual)')
    print(f'Passed: {xor_out == xor_out_actual}')
    print('-------')
