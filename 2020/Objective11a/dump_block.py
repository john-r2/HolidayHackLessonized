from naughty_nice import *

c2 = Chain(load=True, filename='blockchain.dat')

# block 129459 mentions Jack Frost

for index, blk in enumerate(c2.blocks):
    if blk.index == 129459:
        print(blk)
        filename = str(blk.index) + '.bin'
        c2.save_a_block(index, filename)

