import random
import hashlib

class Process:
    def __init__(self, id, shared):
        self.id = id
        self.shared = shared

    def approximate_agreement(self, inp, s):
        i = inp
        for r in range(1, s+1):
            self.shared[r][i % 2] = i
            yield
            i_tag = self.shared[r][(i+1) % 2]
            yield
            if i_tag == None:
                i = 2*i
            else:
                i = i + i_tag
        return i

    def treshold_conciliator(self, inp, f, s):
        i = self.approximate_agreement(inp, s)
        return f(i)


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
    """
    Calculate the SHA-256 hash of a bit string.

    Args:
        bit_string (str): A string containing only '0' and '1' characters

    Returns:
        str: The SHA-256 hash of the bit string as a hexadecimal string
    """
    if not all(bit in '01' for bit in bit_string):
        raise ValueError("Input must be a string containing only '0' and '1' characters")

    # Convert bit string to bytes
    # First, pad the bit string if necessary to ensure its length is a multiple of 8
    padded_length = ((len(bit_string) + 7) // 8) * 8
    padded_bits = bit_string.ljust(padded_length, '0')

    # Convert each 8-bit chunk to a byte
    bytes_array = bytearray()
    for i in range(0, len(padded_bits), 8):
        byte_bits = padded_bits[i:i + 8]
        byte_value = int(byte_bits, 2)
        bytes_array.append(byte_value)

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(bytes_array)

    # Return the hash as a hexadecimal string
    return sha256_hash.hexdigest()

def preprocess(l, T, m, k=256):
    if T > l:
        raise Exception("T must be less than l")
    if k > m:
        raise Exception("k must be less than m")

    C = [[None]*l]*m
    P = [[None]*l]*k

    for i in range(1, l):
        P[i] = random_bit_string(m)
        ri = random_bit_string(k)
        ai = int(i > T)

        if xor_bits(ri) != ai:
            ri = flip_bit(ri, random.randint(k))

        yi = P[i] + ri
        C[i] = sha256_of_bits(yi)
    return C, P