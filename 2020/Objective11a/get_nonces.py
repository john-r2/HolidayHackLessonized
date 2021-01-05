from naughty_nice import *

c2 = Chain(load=True, filename='blockchain.dat')

with open('nonces', 'a') as fh:
    for blk in c2.blocks:
        fh.write(str(blk.nonce) + '\n')
