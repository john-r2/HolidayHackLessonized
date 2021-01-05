#This one loads the first 312 nonces (624 32-bit nonces)
#  after the offset
#  and checks that the predictions match the nonces after that

from mt19937 import mt19937, untemper

# create our own version of an MT19937 PRNG.
myprng = mt19937(0)

# read the nonces
with open('nonces') as fh:
    nonces = fh.readlines()
nonces = [int(s) for s in nonces]

print('There are {} nonces'.format(len(nonces)))

# if offset is 0 we start at the first nonce
offset = 0

# just grab the 312 nonces we need for prediction
last_nonces = nonces[offset:312 + offset]

# assume 64-bit nonces are made by concatenating 32-bit nonces
# will try lower32 bits first, then upper32 bits
# for upper32, shift right 32 bits to get the top 32 bits
# for lower 32 use a mask to remove everything but the bottom 32 bits

# load the nonces into MT
for index, nonce in enumerate(last_nonces):
    upper32 = nonce >> 32
    lower32 = nonce & 0xffffffff
    myprng.MT[index * 2] = untemper(lower32)
    myprng.MT[index * 2 + 1] = untemper(upper32)
 
# recover the 64-bit nonce by shifting the upper prediction 32 bits right
#   and adding it to the lower prediction.

for i in range(312 + offset, 314 + offset):
    pred_lower = myprng.extract_number()
    pred_upper = myprng.extract_number()
    print('With index {0}, the two 32-bt predictions are {1} and {2}'.format(i, pred_lower, pred_upper))
    print('Actual Nonce {}'.format(nonces[i]))
    print('Predicted N. {}'.format((pred_upper << 32) + pred_lower))
    print('\n')


