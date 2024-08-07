import numpy as np
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def flip_one_bit(message):
    byte_index = np.random.randint(0, len(message))
    bit_index = np.random.randint(0, 8)
    message[byte_index] ^= 1 << bit_index
    return message


def encrypt_ecb(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(message)


def encrypt_cbc(message, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(message), iv


def hamming_distance(mes1, mes22):
    return sum(bin(m1 ^ m2).count('1') for m1, m2 in zip(mes1, mes22))

# ---------------------------------------------message generation---------------------------------------------
num_pairs = 35  # number of pairs
msg_length_bytes = 32  # message length in bytes (256bits=32bytes)

# generate random messages
messages = np.random.randint(0, 256, size=(num_pairs, msg_length_bytes), dtype=np.uint8)

flipped_messages = np.empty_like(messages)
for i, msg in enumerate(messages):
    msg_copy = msg.copy()
    flipped_msg = flip_one_bit(msg_copy)
    flipped_messages[i] = flipped_msg

messages_bytes = [msg.tobytes() for msg in messages]
flipped_messages_bytes = [msg.tobytes() for msg in flipped_messages]

# AES key (16 bytes = 128 => AES-128)
key = get_random_bytes(16)

# ---------------------------------------------encrypt messages---------------------------------------------
ecb_cipher_texts = [encrypt_ecb(msg, key) for msg in messages_bytes]
cbc_cipher_texts_with_iv = [encrypt_cbc(msg, key) for msg in messages_bytes]
# list for final version: removing the iv's from messages_bytes
cbc_cipher_texts = []

# Loop through each pair (ciphertext, iv)
for item in cbc_cipher_texts_with_iv:
    # first element is the ciphertext and the second is the IV
    ciphertext = item[0]  # Extract ciphertext
    cbc_cipher_texts.append(ciphertext)

# ---------------------------------------------encrypt flipped messages---------------------------------------------
ecb_flipped_cipher_texts = [encrypt_ecb(msg, key) for msg in flipped_messages_bytes]
cbc_flipped_cipher_texts_with_iv = [encrypt_cbc(msg, key) for msg in flipped_messages_bytes]
# list for final version: removing the iv's from flipped_messages_bytes
cbc_flipped_cipher_texts = []

# Loop through each pair (ciphertext, iv)
for item in cbc_flipped_cipher_texts_with_iv:
    # first element is the ciphertext and the second is the IV
    ciphertext = item[0]  # Extract ciphertext
    cbc_flipped_cipher_texts.append(ciphertext)

# ---------------------------------------------Calculate Hamming distances ECB,CBC---------------------------------------------
ecb_distances = []
# Loop through each pair of original/flipped ciphertexts in ECB mode
for ct1, ct2 in zip(ecb_cipher_texts, ecb_flipped_cipher_texts):
    # Hamming distance for each pair
    distance = hamming_distance(ct1, ct2)
    ecb_distances.append(distance)

cbc_distances = []
# Loop through each pair of original/flipped ciphertexts in CBC mode
for ct1, ct2 in zip(cbc_cipher_texts, cbc_flipped_cipher_texts):
    # Hamming distance for each pair
    distance = hamming_distance(ct1, ct2)
    cbc_distances.append(distance)

average_ecb_distance = sum(ecb_distances) / len(ecb_distances)
average_cbc_distance = sum(cbc_distances) / len(cbc_distances)
print("ECB mode hamming distances:", ecb_distances)
print("CBC mode Hamming distances:", cbc_distances)
print("ECB mode hamming distances average 35 msgs: ",average_ecb_distance)
print("ECB mode hamming distances average 35 msgs: ",average_cbc_distance)
