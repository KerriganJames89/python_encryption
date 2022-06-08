#The program in this file is the individual work of JAMES KERRIGAN

import random
import string
from datetime import datetime
import binascii
import math


random.seed(datetime.now())

'''def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))
'''
'''
def set_bits(num, bit_index, x):
  mask = 1 << bit_index
  num &= ~mask
  if x:
    num |= mask
  return num

def set_bit(value, bit):
  return value | (1<<bit)
'''
'''
def permutate(permutate_table, bits):
  bits_permuted = 0
  for i, j in enumerate(permutate_table):
      bits_val = (bits >> (j-1)) & 1
      bits_permuted = set_bit(bits_permuted, i, bits_val)
  return bits_permuted
'''
'''
def permutate(permutate_table, bits):
  #print (bin(bits))
  bits_permuted = 0
  bit_buffer = 0
  for j in permutate_table[::-1]:
    bit_buffer = (bits >> (j - 1) & 0b1)
    print(j, "=",bin(bit_buffer))
    bits_permuted = (bits_permuted << 1) | (bit_buffer)
    #print (bin(bits_permuted))

  #print (bin(bits_permuted))
  #print ("--------")
  return bits_permuted
'''

  #Permutes given bits with selected permutation table
def permutate(permutate_table, bits, SIZE):
  bits_permutated = 0
  for i in (permutate_table):
      bit_buffer = (bits >> ((SIZE) - i)) & 1
      #print(i, "=",bin(bit_buffer))
      bits_permutated <<= 1
      bits_permutated |= bit_buffer
  return bits_permutated


#Changes ascii into bits (only used for user input)
def to_binary(string):
  bits = 0
  for i, c in enumerate(reversed(string)):
      bits |= ord(c) << (i * 8)
  return bits

#Splits msg and returns left or right half
def split_msg(bits, half):
  if  half == 'L':
    return (bits >> 32) & 0xffffffff

  else: return bits & 0xffffffff

#Left shifts and circular rotates given bits
def left_shift(bits, shift_amount, integer_SIZE):
    mask = 0
    for i in range(integer_SIZE):
      mask <<= 1
      mask |= 1
    return ((bits << shift_amount) & mask) | (bits >> (integer_SIZE - shift_amount))

#Right circular shift
def right_shift(bits, shift_amount, integer_SIZE):
    mask = 0
    for i in range(shift_amount):
        mask <<= 1
        mask |= 1
    return (bits >> shift_amount) | ((bits & mask) << (integer_SIZE - shift_amount))

#Encrypts given msg with a randomly generated key; returns encrypted msg
def encrypt(msg, key):
  
  #Calculates the amount of blocks the program will encrypt/decrypt
  block = (int(math.log2(msg))+1)/64
  if (int(math.log2(msg))+1) % 64 > 0:
    block = block + 1

  #Outer loop seperates blocks greater than 64 bits which are then queued for key-round encryption and does an initial permutation
  for i in range(int(block)):
    
    #Chops up the msg (if greater than 64 bits) into blocks to be encrypted
    msg_bits = (msg >> (i * 64) & (0xffffffffffffffff))

    #Applies initial permutation to the msg binary
    msg_bits = permutate(initial_permutation, msg_bits, 64)

    #Inner loop applies 16 rounds of encryption which includes 16 different key shifts
    for j in range (16):

      #Shifts key once every round
      shifted_key = left_shift(key, j + 1, 56)

      #Permutes given key using PC2 permutatiom (from 56 bits to 48 bits)
      permutated_key = permutate(PC2_permutation, shifted_key, 56)
      msg_bits = DES(msg_bits, permutated_key)

    #Apply one final permutation to current round msg

    msg_bits = permutate(final_permutation, msg_bits, 64)
    print (bin(msg_bits))
    #Concatenate multiple encrypted blocks into one msg
    if i == 0:
      final_msg = msg_bits

    else:
      final_msg = (final_msg << 64 | (msg_bits))

  return final_msg

def decrypt(msg, key):

  #Calculates the amount of blocks the program will encrypt/decrypt
  block = (int(math.log2(msg))+1)/64
  if (int(math.log2(msg))+1) % 64 > 0:
    block = block + 1
    
  #Outer loop seperates blocks greater than 64 bits which are then queued for key-round encryption and does an initial permutation
  for i in range(int(block)):
    
    #Chops up the msg (if greater than 64 bits) into blocks to be encrypted
    msg_bits = (msg >> (i * 64) & (0xffffffffffffffff))

    #Applies initial permutation to the msg binary
    msg_bits = permutate(initial_permutation, msg_bits, 64)

    #Reverse the key to decrypt; I assume we rotate left 16 times then rotate right every increment (without pc-2 being originally applied)
    shifted_key = left_shift(key, 16, 56)

    #Inner loop applies 16 rounds of encryption which includes 16 different key shifts
    for j in range (16):
      
      #Shifts key once every round
      shifted_key = right_shift(key, j + 1, 56)

      #Permutes given key using PC2 permutatiom (from 56 bits to 48 bits)
      permutated_key = permutate(PC2_permutation, shifted_key, 64)
      msg_bits = DES(msg_bits, permutated_key)
    
    #Apply one final permutation to current round msg
    msg_bits = permutate(final_permutation, msg_bits, 64)

    #Concatenate multiple encrypted blocks into one msg
    if i == 0:
      final_msg = msg_bits
    
    else: final_msg = (final_msg << 64) | (msg_bits)

  return final_msg


#Does a single round of DES encryption on given msg
def DES(msg_bits, key):

  #Splits msg into halves
  left_msg = split_msg(msg_bits, 'L')
  right_msg = split_msg(msg_bits, 'R')
  next_round_msg = right_msg

  #Permutes right-hand msg (from 32 bits to 48 bits) with expansion permutation, then XOR with current key
  right_msg = permutate(expansion_permutation, right_msg, 32) ^ key

  #S-block concatenation without strings/lists (what a pain; works though)
  for i in range(8):
    
    inner_bits = (right_msg >> 1 + (i * 6) & 0b1111)
    outer_buffer1 = (right_msg >> 5 + (i * 6) & 0b1)
    outer_buffer2 = (right_msg >> i * 6  & 0b1)
    outer_bits = (outer_buffer1 << 1) | (outer_buffer2)

    #Applies S-box configurations
    buffer_msg1 = (s_box[(outer_bits * 16 + inner_bits)])

    if i == 0:
      buffer_msg2 = buffer_msg1

    else:
      buffer_msg2 = ((buffer_msg2<<4) | buffer_msg1)

      #Permutes right-hand msg (now 32 bits) using P-permutation
      if i == 7: 
        right_msg = permutate(P_permutation, buffer_msg2, 32)

  #Xor left-hand msg and altered right-hand msg to create the final right-hand msg for the round
  right_msg = right_msg ^ left_msg

  #Attach this round's unaltered right-hand msg to the left side of next round's msg with the newely altered msg
  return (next_round_msg << 32) | (right_msg)



initial_permutation = \
[58, 50, 42, 34, 26, 18, 10, 2, 
60, 52, 44, 36, 28, 20, 12, 4, 
62, 54, 46, 38, 30, 22, 14, 6, 
64, 56, 48, 40, 32, 24, 16, 8, 
57, 49, 41, 33, 25, 17, 9, 1, 
59, 51, 43, 35, 27, 19, 11, 3, 
61, 53, 45, 37, 29, 21, 13, 5, 
63, 55, 47, 39, 31, 23, 15, 7]

PC2_permutation = \
[14, 17, 11, 24, 1, 5,
3, 28,	15,	6,	21,	10,
23, 19, 12,	4, 26, 8,
16,	7, 27, 20, 13, 2,
41,	52,	31,	37, 47, 55,
30,	40,	51,	45,	33,	48,
44,	49,	39,	56,	34,	53,
46,	42,	50,	36,	29,	32]

expansion_permutation = \
[32, 1, 2, 3,	4, 5,
4, 5, 6, 7, 8, 9,
8, 9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21,	22, 23,	24,	25,
24, 25,	26,	27, 28, 29,
28, 29,	30,	31, 32,	1]

P_permutation = \
[16, 7, 20, 21, 29, 12, 28, 17,
1, 15, 23, 26, 5, 18, 31, 10,
2, 8, 24, 14, 32, 27, 3, 9,
19, 13, 30, 6, 22, 11, 4, 25]

final_permutation = \
[40, 8, 48, 16, 56, 24, 64,32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41, 9, 49, 17, 57, 25]


s_box = \
[0b1110, 0b0100, 0b1101, 0b0001, 0b0010, 0b1111, 0b1011, 0b1000, 0b0011, 0b1010, 0b0110, 0b1100, 0b0101, 0b1001, 0b0000, 0b0111,
0b0000, 0b1111, 0b0111, 0b0100, 0b1110, 0b0010, 0b1101, 0b0001, 0b1010, 0b0110, 0b1100, 0b1011, 0b1001, 0b0101, 0b0011, 0b1000,
0b0100, 0b0001, 0b1110, 0b1000, 0b1101, 0b0110, 0b0010, 0b1011, 0b1111, 0b1100, 0b1001, 0b0111, 0b0011, 0b1010, 0b0101, 0b0000,
0b1111, 0b1100, 0b1000, 0b0010, 0b0100, 0b1001, 0b0001, 0b0111, 0b0101, 0b1011, 0b0011, 0b1110, 0b1010, 0b0000, 0b0110, 0b1101]

#Generates a random key using datetime
key = ""
for i in range(7):
  key += random.choice(string.ascii_letters)
key = to_binary(key)

while(True):
  print("DES Implementation:")
  print("Enter text to encrypt or type Exit to quit:")
  x = input()
  if x == "quit":
    break

  else: 

    msg = to_binary(x)

    encyrpted_msg = encrypt(msg, key)
    print("Encrypted Text:", binascii.unhexlify('%x' % encyrpted_msg))

    decrypted_msg = bin(decrypt(encyrpted_msg, key))
    print ("Decrypted Text (ascii conversion throws errors):", decrypted_msg)

