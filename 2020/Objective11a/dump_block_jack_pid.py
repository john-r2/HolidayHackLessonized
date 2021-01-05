from naughty_nice import *

c2 = Chain(load=True, filename='blockchain.dat')

# after finding Frost in the docs, did this
#if blk.index == 129459:
#that block says Frost PID is 0000000000012fd1
#see if Frost's PID appears in any other blocks
for index, blk in enumerate(c2.blocks):
    if blk.pid == 0x12fd1 or blk.rid == 0x12fd1:
        print(blk)
        print('Block index {0} appears as Python index {1}'.format(blk.index, index))
        filename = str(blk.index) + '.bin'
        c2.save_a_block(index, filename)

#Frost only appears in 129459
#Python index is 1010
