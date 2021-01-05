from mt19937 import mt19937, untemper

# create our own version of an MT19937 PRNG.
myprng = mt19937(0)

# read the snowball bad attempts
with open('snow_attempts3.txt') as fh:
    snow_nums = fh.readlines()
snow_nums = [int(s) for s in snow_nums]

# load the snowball attempts into Tom's extractor
for i in range(mt19937.n):
    myprng.MT[i] = untemper(snow_nums[i])

# print the 1st 10 'random' numbers
for i in range(10):
    print(myprng.extract_number())
