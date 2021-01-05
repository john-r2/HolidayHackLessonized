# run this from an empty directory as it will generate a lot of files
#   copy naughty_nice.py and blockchain.dat to the same directory

from naughty_nice import *

c2 = Chain(load=True, filename='blockchain.dat')

block_counter = 0
doc_counter = 0

for blk in c2.blocks:
    block_counter += 1
    for i in range(blk.doc_count):
        blk.dump_doc(i)
        doc_counter += 1
print('dumped {0} documents from {1} blocks'.format(doc_counter, block_counter))

