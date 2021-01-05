#!/usr/bin/env python3

'''
So, you want to work with the naughty/nice blockchain?

Welcome!  

This python module is your first step in that process. It will introduce you to how the Naughty/Nice
blockchain is structured and how we at the North Pole use blockchain technology. The North Pole
has been using blockchain technology since Santa first invented it back in the 1960's. (Jolly
prankster that he is, Santa posted a white paper on the Internet that he wrote under a pseudonym
describing a non-Naughty/Nice application of blockchains a dozen or so years back. It caused quite
a stir...)

Important note: This module will NOT allow you to add content to the Official Naughty/Nice Blockchain!
That can only be done through the Official Naughty/Nice Website, which passes new blocks to the Official
Santa Signature System (OS3) that applies a digital signature to the content of each block before it is
added to the chain. Only blocks whose contents have been digitally signed by that system are placed on
the Naughty/Nice blockchain.

Note: If you're authorized to use the Official Naughty/Nice website, you will have been given a login and
password for that site after completing your training as a part of Elf University's "Assessing and
Evaluating Human Behavior for Naughty/Niceness" Curriculum.

This code is used to introduce how blocks/chains are created and allow you to view and/or validate 
portions (or the entirety) of the Official Naughty/Nice Blockchain.

A blockchain, while a part of the whole cryptocurrency "fad" that a certain pseudonym-packing North Pole
resident appears to have begun, are certainly not limited to that use. A blockchain can be used anywhere
that a record of information or transactions need to be maintained in a way that cannot be altered. And
really, what information is more important (and necessarily unalterable) than acts of Naughty/Niceness?

A blockchain works by linking each record together with the previous record. Each block's data contains
a cryptographic hash of the previous block's data. Because a block cannot be altered without altering
the cryptographic hash of its contents, any alteration of the data within a block will be immediately
evident, because every following block will no longer be valid.

In addition to this built-in property of a blockchain, the Official Naughty/Nice Blockchain has a few
other safeguards. The cryptographic hash of each block is signed using the Official Santa Signature
System (OS3). Currently, the Official Naughty/Nice Blockchain uses MD5 as its hashing algorithm, but
plans are in place to move to SHA256 in 2021. This update is part of a phased process to modernize
the blockchain code. In 2019, the entire blockchain system was ported from the original COBOL code to
Python3. Because of concerns about hash collisions in MD5, in the new Python3 code, a 64-bit random 
"nonce" was added to the beginning of each block at the time of creation.

This module represents a portion of the most current blockchain codebase. It consists of two classes,
one for the creation of blocks, called Block(), and one for the creation, examination, and verification of
chains of blocks, called Chain(). 

The following is an overview of the functionality provided by these classes:

The Chain() class is where most blockchain work is performed. It is designed to be as "block-agnostic"
as possible, so it can be used with blocks that hold different types of data. To use a different type
of block, you simply replace (or subclass) the Block() class. For this to work, there are several
functions that MUST be supplied by the Block() class. Let's take a look at those.

The Block() class MUST supply the following functions, used by the Chain() class:

    create_genesis_block() - This creates a very special block used at the beginning of the blockchain,
    and known as the "genesis" block. Because it has no previous block to reference it is, by definition,
    always considered valid. This block uses an agreed-upon, fake previous hash value.

    verify_types() - Because the Chain() class is block-agnostic, it needs the Block() class to validate
    that a block contains valid data. This function returns True or False.

    block_data() - a function that returns a representation of all of the data in the block that is to
    be hashed and signed. The data is returned as a Python3 bytes object.

    full_block_data() - a function that returns a representation of the entire block, including any
    hashes and signatures. A hash of this data is what is used as the "previous hash" value in the
    subsequent block. This data is returned as a Python3 bytes object. This function is also used
    when saving either the entire blockchain to a file, or a single block to a file

    load_a_block([filehandle]) - this function takes a filehandle and returns a block at a time for
    addition to the block chain. This function DOES NOT verify blocks. This function throws a
    Value_Error exception when it either encounters the end of the file or unparsable data.

The Naughty/Nice Block() class also defines a utility function:

    dump_doc([document number]) - this will dump the indicated supporting document to a file named
    as <block_index>.<data_type_extension>. Note: this function will overwrite any existing file 
    with that name, so if there are multiple documents (there can be up to 9) of the same type 
    affixed to a record, it is the responsibility of the calling process to rename them as appropriate.

The Chain() class provides the following functions:

    add_block([block_data]) - passes a block_data dictionary to the Block() initialization code.
    This function, being "block-agnostic" simply passes the block_data along. It is up to the Block()
    initialization code to validate this data.

    verify_chain([public_key], <beginning hash>) - steps through every block in the chain and
    verifies that the data in each block is of the correct type, that the block index is correct,
    that the block contains the correct hash for the previous block, and that the block signature
    is a valid signature based on the hash of the block data. It then hashes the full block for use
    as the "previous hash" on the next block. This returns True or False. (If False, it prints
    information about what, specific, issues were found and the block that triggered the issue.)
    Note: If you're working with a portion of the block chain that does not begin with a genesis
    block, you'll need to provide a value for the previous block's hash for this function to
    work.

    save_a_block(index, <filename>) - saves the block at index to the filename provided, or to 
    "block.dat" if no filename is given.

    save_chain(<filename>) - saves the chain to the filename provided, or to "blockchain.dat" if
    no filename is given.

    load_chain(<filename>) - loads a chain from the filename provided, or from "blockchain.dat" if
    no filename is given. This returns the count of blocks loaded. This DOES NOT verify that the
    data loaded is a valid blockchain. It is recommended to call verify_chain() immediately after
    loading a new chain.   

An overview of how we process the Official Naughty/Nice Blockchain:

There are approximately 7.8 billion people and magical beings on Earth, and each one is tracked
24 hours a day throughout the year by a fleet of Elves-On-The-Shelves. While those elves are
clearly visible during the Holiday season, don't be fooled into believing that we're only tracking
Naughty/Niceness at that time. On average, each of the billions of subjects that we monitor are
performing some sort of Naughty or Nice activity that rises to the level of being scored on the
blockchain around 2.1 times per week. Keeping track of all of that activity on a single blockchain
would be incredibly processing intensive (that would be ~1^12 blocks/year, or 32,000 blocks/second),
so we've broken our record-keeping into 1,000 different blockchains. If you do the math, you'll find
that each of the blockchains is now responsible for between 1,500 and 2000 blocks per minute, which
is a reasonable load. A separate database keeps track of which Personal ID (pid) is assigned to each
of the blockchains.

Throughout the year, we periodically run each of the chains to determine who is the best (and worst)
of our subjects. While only the final Holiday run is used to determine who is getting something
good in their stockings and who is getting a lump of coal, it's always interesting to see a listing
of the Nicest and Naughtiest folks out there. 

Please note: Wagering on the results of the Official Naughty/Nice Blockchain is STRICTLY PROHIBITED.

If you intend to use your access to the Official Naughty/Nice Blockchain code to facilitate any sort
of gambling, you will be racking up a whole bunch of Naughtiness points. YOU HAVE BEEN WARNED! (I'm
looking at you, Alabaster Snowball...)

For this reason, we have not provided any code that will perform a computation of Naughty/Nice
points. Additionally, for privacy reasons, there is also no code to pull the records associated
with specific individuals from this list. While the creation of that code would not be difficult,
you are honor-bound to use your access to this list for only good and noble purposes.

Signing Keys - Information

We have provided you with an example private key that you can use when generating your own blockchains
for test purposes. This private key (which also contains the public key information) is called 
private.pem.

Additionally, we have provided you with a copy of the public key used to verify the Official
Naughty/Nice Blockchain. This is the public key component of the private key used by the Official
Santa Signature System (OS3) to sign blocks on the Official Naughty/Nice Blockchain. This key
is contained in the file official_public.pem.
'''

import random
from Crypto.Hash import MD5, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode
import binascii
import time

genesis_block_fake_hash = '00000000000000000000000000000000'

data_types = {1:'plaintext', 2:'jpeg image', 3:'bmp image', 4:'gif image', 5:'PDF', 6:'Word', 7:'PowerPoint', 8:'Excel', 9:'tiff image', 10:'MP4 video', 11:'MOV video', 12:'WMV video', 13:'FLV video', 14:'AVI video', 255:'Binary blob'}
data_extension = {1:'txt', 2:'jpg', 3:'bmp', 4:'gif', 5:'pdf', 6:'docx', 7:'pptx', 8:'xlsx', 9:'tiff', 10:'mp4', 11:'mov', 12:'wmv', 13:'flv', 14:'avi', 255:'bin'}

Naughty = 0
Nice = 1

class Block():
    def __init__(self, index=None, block_data=None, previous_hash=None, load=False, genesis=False):
        if(genesis == True):
            return None
        else:
            self.data = []
            if(load == False):
                if all(p is not None for p in [index, block_data['documents'], block_data['pid'], block_data['rid'], block_data['score'], block_data['sign'], previous_hash]):
                    self.index = index
                    if self.index == 0:
                        self.nonce = 0 # genesis block
                    else:
                        self.nonce = random.randrange(0xFFFFFFFFFFFFFFFF)                
                    self.data = block_data['documents']
                    self.previous_hash = previous_hash
                    self.doc_count = len(self.data)
                    self.pid = block_data['pid']
                    self.rid = block_data['rid']
                    self.score = block_data['score']
                    self.sign = block_data['sign']
                    now = time.gmtime()
                    self.month = now.tm_mon
                    self.day = now.tm_mday
                    self.hour = now.tm_hour
                    self.minute = now.tm_min
                    self.second = now.tm_sec
                    self.hash, self.sig = self.hash_n_sign()
                else:
                    return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        s = 'Chain Index: %i\n' % (self.index)
        s += '              Nonce: %s\n' % ('%016.016x' % (self.nonce))
        s += '                PID: %s\n' % ('%016.016x' % (self.pid))
        s += '                RID: %s\n' % ('%016.016x' % (self.rid))
        s += '     Document Count: %1.1i\n' % (self.doc_count)
        s += '              Score: %s\n' % ('%08.08x (%i)' % (self.score, self.score))
        n_n = 'Naughty'
        if self.sign > 0:
            n_n = 'Nice'
        s += '               Sign: %1.1i (%s)\n' % (self.sign, n_n)
        c = 1
        for d in self.data:
            s += '         Data item: %i\n' % (c)
            s += '               Data Type: %s (%s)\n' % ('%02.02x' % (d['type']), data_types[d['type']])
            s += '             Data Length: %s\n' % ('%08.08x' % (d['length']))
            s += '                    Data: %s\n' % (binascii.hexlify(d['data']))
            c += 1
        s += '               Date: %s/%s\n' % ('%02.02i' % (self.month), '%02.02i' % (self.day))
        s += '               Time: %s:%s:%s\n' % ('%02.02i' % (self.hour), '%02.02i' % (self.minute), '%02.02i' % (self.second))
        s += '       PreviousHash: %s\n' % (self.previous_hash)
        s += '  Data Hash to Sign: %s\n' % (self.hash)
        s += '          Signature: %s\n' % (self.sig)
        return(s)

    def full_hash(self):
        hash_obj = MD5.new()
        hash_obj.update(self.block_data_signed())
        return hash_obj.hexdigest()

    def hash_n_sign(self):
        hash_obj = MD5.new()
        hash_obj.update(self.block_data())
        signer = PKCS1_v1_5.new(private_key)
        return (hash_obj.hexdigest(), b64encode(signer.sign(hash_obj)))

    def block_data(self):
        s = (str('%016.016x' % (self.index)).encode('utf-8'))
        s += (str('%016.016x' % (self.nonce)).encode('utf-8'))
        s += (str('%016.016x' % (self.pid)).encode('utf-8'))
        s += (str('%016.016x' % (self.rid)).encode('utf-8'))
        s += (str('%1.1i' % (self.doc_count)).encode('utf-8'))
        s += (str(('%08.08x' % (self.score))).encode('utf-8'))
        s += (str('%1.1i' % (self.sign)).encode('utf-8'))
        for d in self.data:
            s += (str('%02.02x' % d['type']).encode('utf-8'))
            s += (str('%08.08x' % d['length']).encode('utf-8'))
            s += d['data']
        s += (str('%02.02i' % (self.month)).encode('utf-8'))
        s += (str('%02.02i' % (self.day)).encode('utf-8'))
        s += (str('%02.02i' % (self.hour)).encode('utf-8'))
        s += (str('%02.02i' % (self.minute)).encode('utf-8'))
        s += (str('%02.02i' % (self.second)).encode('utf-8'))
        s += (str(self.previous_hash).encode('utf-8'))
        return(s)

    def block_data_signed(self):
        s = self.block_data()
        s += bytes(self.hash.encode('utf-8'))
        s += self.sig
        return(s)

    def load_a_block(self, fh):
        self.index = int(fh.read(16), 16)
        self.nonce = int(fh.read(16), 16)
        self.pid = int(fh.read(16), 16)
        self.rid = int(fh.read(16), 16)
        self.doc_count = int(fh.read(1), 10)
        self.score = int(fh.read(8), 16)
        self.sign = int(fh.read(1), 10)
        count = self.doc_count
        while(count > 0):
            l_data = {}
            l_data['type'] = int(fh.read(2),16)
            l_data['length'] = int(fh.read(8), 16)
            l_data['data'] = fh.read(l_data['length'])
            self.data.append(l_data)
            count -= 1
        self.month = int(fh.read(2))
        self.day = int(fh.read(2))
        self.hour = int(fh.read(2))
        self.minute = int(fh.read(2))
        self.second = int(fh.read(2))
        self.previous_hash = str(fh.read(32))[2:-1]
        self.hash = str(fh.read(32))[2:-1]
        self.sig = fh.read(344)
        return self

    def create_genesis_block(self):
        block_data = {}
        documents = []
        doc = {}
        doc['data'] = bytes('Genesis Block'.encode('utf-8'))
        doc['type'] = 1
        doc['length'] = len(doc['data'])
        documents.append(doc)
        block_data['documents'] = documents
        block_data['pid'] = 0
        block_data['rid'] = 0
        block_data['score'] = 0
        block_data['sign'] = Nice
        b = Block(0, block_data, genesis_block_fake_hash)
        return b

    def verify_types(self):  # check data types of all info in a block
        rv = True
        instances = [self.index, self.nonce, self.pid, self.rid, self.month, self.day, self.hour, self.minute, self.second, self.previous_hash, self.score, self.sign]
        types = [int, int, int, int, int, int, int, int, int, str, int, int]
        if not sum(map(lambda inst_, type_: isinstance(inst_, type_), instances, types)) == len(instances):
            rv = False
        for d in self.data:
            if not isinstance(d['type'], int):
                rv = False
            if not isinstance(d['length'], int):
                rv = False
            if not isinstance(d['data'], bytes):
                rv = False
        return rv

    def dump_doc(self, doc_no):
        filename = '%s.%s' % (str(self.index), data_extension[self.data[doc_no - 1]['type']])
        with open(filename, 'wb') as fh:
            d = self.data[doc_no - 1]['data']
            fh.write(d)
        print('Document dumped as: %s' % (filename))


class Chain():
    index = 0
    initial_index = 0
    last_hash_value = ''
    def __init__(self, load=False, filename=None):
        if not load:
            self.blocks = [Block(genesis=True).create_genesis_block()]
            self.last_hash_value = self.blocks[0].full_hash()
        else:
            self.blocks = []
            self.load_chain(filename)
            self.index = self.blocks[-1].index
            self.initial_index = self.blocks[0].index

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def add_block(self, block_data):
        self.index += 1
        b = Block(self.index, block_data, self.last_hash_value)
        self.blocks.append(b)
        self.last_hash_value = b.full_hash() 

    def verify_chain(self, publickey, previous_hash=None):
        flag = True
        # unless we're explicitly told what the initial last hash should be, we assume that
        # the initial block will be the genesis block and will have a fixed previous_hash
        if previous_hash is None:
            previous_hash = genesis_block_fake_hash
        for i in range(0, len(self.blocks)):  # assume Genesis block integrity
            block_no = self.blocks[i].index
            if not self.blocks[i].verify_types():
                flag = False
                print(f'\n*** WARNING *** Wrong data type(s) at block {block_no}.')
            if self.blocks[i].index != i + self.initial_index:
                flag = False
                print(f'\n*** WARNING *** Wrong block index at what should be block {i + self.initial_index}: {block_no}.')
            if self.blocks[i].previous_hash != previous_hash:
                flag = False
                print(f'\n*** WARNING *** Wrong previous hash at block {block_no}.')
            hash_obj = MD5.new()
            hash_obj.update(self.blocks[i].block_data())
            signer = PKCS1_v1_5.new(publickey)
            if signer.verify(hash_obj, b64decode(self.blocks[i].sig)) is False:
                flag = False
                print(f'\n*** WARNING *** Bad signature at block {block_no}.')
            if flag == False:
                print(f'\n*** WARNING *** Blockchain invalid from block {block_no} onward.\n')
                return False
            previous_hash = self.blocks[i].full_hash()
        return True

    def save_a_block(self, index, filename=None):
        if filename is None:
            filename = 'block.dat'
        with open(filename, 'wb') as fh:
            fh.write(self.blocks[index].block_data_signed())

    def save_chain(self, filename=None):
        if filename is None:
            filname = 'blockchain.dat'
        with open(filename, 'wb') as fh:
            i = 0
            while(i < len(self.blocks)):
                fh.write(self.blocks[i].block_data_signed())
                i += 1

    def load_chain(self, filename=None):
        count = 0
        if filename is None:
            filename = 'blockchain.dat'
        with open(filename, 'rb') as fh:
            while(1):
                try:
                    self.blocks.append(Block(load=True).load_a_block(fh))
                    self.index = self.blocks[-1].index
                    count += 1
                except ValueError:
                    return count

if __name__ == '__main__':
    with open('private.pem', 'rb') as fh:
        private_key = RSA.importKey(fh.read())
    public_key = private_key.publickey()
    c1 = Chain()
    for i in range(9):
        block_data = {}
        documents = []
        doc = {}
        doc['data'] = bytes(('This is block %i of the naughty/nice blockchain.' % (i)).encode('utf-8'))
        doc['type'] = 1
        doc['length'] = len(doc['data'])
        documents.append(doc)
        block_data['documents'] = documents
        block_data['pid'] = 123 # this is the pid, or "person id," that the block is about
        block_data['rid'] = 456 # this is the rid, or "reporter id," of the reporting elf
        block_data['score'] = 100 # this is the Naughty/Nice score of the report
        block_data['sign'] = Nice # this indicates whether the report is about naughty or nice behavior
        c1.add_block(block_data)
    print(c1.blocks[3])
    print('C1: Block chain verify: %s' % (c1.verify_chain(public_key)))

# Note: This is how you would load and verify a blockchain contained in a file called blockchain.dat
#
#    with open('official_public.pem', 'rb') as fh:
#        official_public_key = RSA.importKey(fh.read())
#    c2 = Chain(load=True, filename='blockchain.dat')
#    print('C2: Block chain verify: %s' % (c2.verify_chain(official_public_key)))
#    print(c2.blocks[0])
#    c2.blocks[0].dump_doc(1)
