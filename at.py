# numlines = int(input("Enter the number of line(s): "))

# ch = 0

# for i in range(numlines):
#     line = ''
#     for j in range(numlines - i - 1):
#         line += ' '
#     for j in range(i + 1):
#         line += chr(ch + 65) + ' '
#         ch += 1
#         if ch > 25:
#             ch -= 26 
#     print(line)

# valid keeps track of whether ID is still valid at this point in the code
valid = True
id = input("ID num > ")

# if the id's length is not 18, print out Fake ID text, and set valid to False
if len(id) != 18:
    print("Fake ID: incorrect length")
    valid = False
else:
    # if id has the correct length, now we check if all digits in id are valid
    
    for char in range(len(id) - 1):
        ch = id[char]
        # this makes sure that all the digits in the first 17 bits are numbers 0 to 9
        if ch < '0' or ch > '9':
            # if not, it prints out the Fake ID text, sets valid to false, and then breaks the loop
            print("Fake ID: invalid character(s)")
            valid = False
            break
    ch = id[-1]
    # if the id is still valid, we check the last bit.
    # if the last bit is a number, we are good. 
    # If it is not a number, and its not x, then print out Fake ID text, and set valid to false. 
    if valid and (ch < '0' or ch > '9'):
        if ch != 'x':
            print("Fake ID: invalid character(s)")
            valid = False

    # if the id is still valid (correct length, correct characters), we check checksum
    if (valid):
        sum = 0
        for char in range(len(id) - 1):
            # the weight is calculated as 2^(17 - i) % 11
            weight = 2**(len(id) - 1 - char) % 11
            # sum is sumed over all digits times their weights
            sum += int(id[char]) * weight
        # checksum is defined as (12 - (S % 11)) % 11
        checksum = (12 - (sum % 11)) % 11
        # ch tracks the last digit of the id.
        ch = id[-1]
        # a last digit of x corresponds to a checksum of 10.
        if ch == 'x':
            ch = '10'
        # if the last digit of x is different than the checksum value
        # then print out fake id text, and set valid to false.
        if checksum != int(ch):
            print("Fake ID: invalid checksum")
            valid = False

# after all our tests, if the id is still valid, then no fake id text was printed.
# then, this id is a valid id.
if valid:
    print("Valid ID")
    