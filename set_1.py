from collections import Counter, namedtuple
from math import log
import string

ScoredOutcome = namedtuple('ScoredOutcome', ['outcome', 'score'])

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

def xor_by_key(byte_array, key):
    return [byte ^ key for byte in byte_array]

def number_to_byte_array(x):
    byte_array = []
    while x != 0:
        byte_array.append(x & 0b11111111)
        x = x >> 8
    return list(reversed(byte_array))

def xor_hex(hex_a, hex_b):
    bits = xor_numbers(hex_to_number(hex_a), hex_to_number(hex_b))
    return bits_to_hex(bits)

def xor_numbers(a, b):
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

def read_frequencies(path, sep='\t'):
    frequencies = Counter()
    with open(path) as f:
        for line in f:
            char, freq = line.split(sep)
            frequencies[char.lower()] = float(freq) / 100
    return frequencies

def count_characters_from_file(path, normalize=True):
    frequency = Counter()
    total = 0
    with open(path) as f:
        for line in f:
            frequency = frequency + count_characters(line.lower(), normalize=False)
    if normalize:
        frequency = normalize_counts(frequency)
    return frequency

def count_characters(text, normalize=True):
    frequency = Counter(text)
    if normalize:
        frequency = normalize_counts(frequency)
    return frequency

def normalize_counts(counts):
    frequency = Counter(counts)
    total = sum(counts.values())
    for item, count in counts.items():
        frequency[item] = count / total
    return frequency

def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line

def kl_divergence(P,Q):
    return sum(p * log(p / q) if q > 0 and p > 0 else float('inf') for p,q in zip(P,Q))

def chi2_distance(P,Q):
    return sum((p - q) ** 2 / p if p > 0 else float('inf') for p,q in zip(P,Q))

def find_best_byte_key(byte_array, character_frequencies):
    best = ScoredOutcome(-1,float('inf'))
    for key in range(255):
        text = decode_as_text(byte_array, key)
        corpus_dist, text_dist = character_distributions(text, character_frequencies)
        score = chi2_distance(corpus_dist, text_dist)
        if score < best.score:
            best = ScoredOutcome(key, score)
    return best

def decode_as_text(byte_array, key):
    return ''.join(chr(x) for x in xor_by_key(byte_array, key))

def character_distributions(text, character_frequencies):
    frequencies = count_characters(text)
    corpus_dist = [character_frequencies.get(char, 0.000000001) for char in frequencies.keys()]
    text_dist = frequencies.values()
    return (corpus_dist, text_dist)

if __name__ == '__main__':
    print('cryptopals.com challenges')
    print('=========================')

    # set 1-1
    hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    base64_out = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    base64_out_actual = hex_to_base64(hex_string)
    print(f'Set 1-1: Base64 ({is_passed(base64_out == base64_out_actual)})')
    print(f'In: \t{hex_string}')
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

    # set 1-3
    hex_string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    corpus_frequencies = count_characters_from_file('bible.txt')
    byte_array = bytearray.fromhex(hex_string)
    key, score = find_best_byte_key(byte_array, corpus_frequencies) 
    text = decode_as_text(byte_array, key)
    print(f'Set 1-3: Single Byte Cypher')
    print(f'In: \t{hex_string}')
    print(f'Out:\t{text} (key: {key}, score(X²): {score})')
    print('-------')

    #set 1-4
    line_number = -1
    line_text = ''
    best = ScoredOutcome(-1, float('inf'))
    for i, line in enumerate(read_lines('1-4.txt')):
        key, score = find_best_byte_key(bytearray.fromhex(line), corpus_frequencies)
        if score < best.score:
            best = ScoredOutcome(key, score)
            line_number = i
            line_text = line
    line_text = decode_as_text(bytearray.fromhex(line_text), best.outcome)
    print(f'Set 1-4: Decoded Stuff')
    print(f'Out:\t[{line_number}]:{line_text[:-1]} (key: {best.outcome}, score(X²): {best.score})')
    print('-------')
