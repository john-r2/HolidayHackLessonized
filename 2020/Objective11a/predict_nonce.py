#This  loads the last 312 nonces (624 32-bit nonces)
#  and predicts the next 6 nonces after that

from mt19937 import mt19937, untemper

# create our own version of an MT19937 PRNG.
myprng = mt19937(0)

# read the nonces saved by get_nonces.py
with open('nonces') as fh:
    nonces = fh.readlines()
nonces = [int(s) for s in nonces]

# we just need the last 624 32-bit nonces
# since these nonces are 64 bits, that is 312
last_nonces = nonces[(len(nonces)-312):]

# for upper32, shift right 32 bits to get the top 32 bits
# for lower 32 use a mask to remove everything but the bottom 32 bits
# load the two 32-bit nonces into MT

for index, nonce in enumerate(last_nonces):
    upper32 = nonce >> 32
    lower32 = nonce & 0xffffffff
    myprng.MT[index * 2] = untemper(lower32)
    myprng.MT[index * 2 + 1] = untemper(upper32)
 
# We know that the last block is index 129996
#  so grab 6 nonces after that
for i in range(129997, 130003):
    pred_lower = myprng.extract_number()
    pred_upper = myprng.extract_number()
    combined = (pred_upper << 32) + pred_lower
    print('Index {0}, lower = {2}, upper = {3}, predicted nonce is {1}'\
        .format(i, hex(combined), hex(pred_lower), hex(pred_upper)))
    
    
    
