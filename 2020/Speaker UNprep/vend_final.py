# this is to build a list of characters to crack the key
# delete vending_machine.json to make it force a new password
#
# Copy the data when this script requests input
# Paste it into the ./vending_machine request for password
# When the vending_machine stops, copy the password in
#   vending_machine.json
# Paste the back into this script

# got lucky and hit the answer on my first attempt at period
period = 8

# Probably didn't need to break the password into three parts,
#   but why not?

# AAAAAAAA through ZZZZZZZZ
out = ''
for i in range(65, 91):
    out += chr(i) * period
pwd_upper = input('password upper\n{}\n'.format(out))

# aaaaaaaa through zzzzzzzz
out = ''
for i in range(97, 123):
    out += chr(i) * period
pwd_lower = input('password lower\n{}\n'.format(out))

# 00000000 through 99999999
out = ''
for i in range(48, 58):
    out += chr(i) * period
pwd_digit = input('password digit\n{}\n'.format(out))

# Add the results to make one string
pwd = pwd_upper + pwd_lower + pwd_digit

key_period = 8
a = [''] * key_period

# break the password into separate strings since it
#  repeats--number of strings is the key_period
for i in range(0, len(pwd), key_period):
    for j in range(key_period):
        a[j] += pwd[i+j]
        
# create the symbol set, A-Z a-z 0-9
SymSet = ''
for i in range(65, 91):
    SymSet += chr(i)

for i in range(97, 123):
    SymSet += chr(i)

for i in range(48, 58):
    SymSet += chr(i)

print('Sample translation for the first letter, sanity check')
print(SymSet)
print(a[0])

# Finally, crack the password
pwd2crack = 'LVEdQPpBwr'
password = ''

for j in range(len(pwd2crack)):
    i = j % key_period  #index to key, i, repeats
    ltrIndex = a[i].find(pwd2crack[j])
    password += SymSet[ltrIndex]
    print(i, j, pwd2crack[j], ltrIndex, SymSet[ltrIndex])
print(password)
