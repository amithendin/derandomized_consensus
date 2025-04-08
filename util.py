import hashlib
import random


def random_bit_string(length):
    if length < 0:
        raise ValueError("Length must be a non-negative integer")

    return ''.join(random.choice(['0', '1']) for _ in range(length))


def xor_bits(bit_string):
    if not bit_string:
        raise ValueError("Input bit string cannot be empty")

    if not all(bit in '01' for bit in bit_string):
        raise ValueError("Input must be a string containing only '0' and '1' characters")

    # Initialize result with the first bit
    result = int(bit_string[0])

    # XOR with each subsequent bit
    for bit in bit_string[1:]:
        result ^= int(bit)

    return result


def flip_bit(bit_string, index):
    if not bit_string:
        raise ValueError("Input bit string cannot be empty")

    if not all(bit in '01' for bit in bit_string):
        raise ValueError("Input must be a string containing only '0' and '1' characters")

    if index < 0 or index >= len(bit_string):
        raise IndexError(f"Index {index} out of range for bit string of length {len(bit_string)}")

    # Convert the bit string to a list for easy manipulation
    bits = list(bit_string)

    # Flip the bit at the specified index
    bits[index] = '1' if bits[index] == '0' else '0'

    # Convert back to a string and return
    return ''.join(bits)

def sha256_of_bits(bit_string):
    if not all(bit in '01' for bit in bit_string):
        raise ValueError("Input must be a string containing only '0' and '1' characters")

    padded_length = ((len(bit_string) + 7) // 8) * 8
    padded_bits = bit_string.ljust(padded_length, '0')

    bytes_array = bytearray()
    for i in range(0, len(padded_bits), 8):
        byte_bits = padded_bits[i:i + 8]
        byte_value = int(byte_bits, 2)
        bytes_array.append(byte_value)

    sha256_hash = hashlib.sha256(bytes_array)

    return sha256_hash.hexdigest()

def H(x,y):
    x_str = str(x).encode('utf-8')
    y_str = str(y).encode('utf-8')
    x_hash = hashlib.sha256(x_str).digest()
    y_hash = hashlib.sha256(y_str).digest()

    combined_hash = x_hash + y_hash

    result_bit = 0
    for byte in combined_hash:
        for i in range(8):
            bit = (byte >> i) & 1
            result_bit ^= bit

    return result_bit


def find_i_tuple(tuple_set, i, v):
    for t in tuple_set:
        if t[i] == v:
            return t
    return None
