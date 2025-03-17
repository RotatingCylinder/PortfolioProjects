# code for caesar cipher tool
# every character in the message is offset by an integer key value
from curses.ascii import isalpha

# alphabet_size is for alphabets that don't use every latin character, such as the Italian alphabet
# special_case determines if characters not in the latin alphabet are included

def caesar_encrypt(msg, key, special_case = True,
                    alphabet_size = 26, upper_case = True):

    encrypted_msg = ""

    # check if ascii_diff should be for upper or lower case
    if upper_case:
        ascii_diff = ord('A')
    else:
        ascii_diff = ord('a')


    for x in msg:
        # check if spaces and special characters should be included
        if not isalpha(x) & special_case == True:
            encrypted_msg += x
        else:
            val = ord(x) - ascii_diff
            encrypted_val = (val + key) % alphabet_size
            # mod alphabet_size ensures ascii values loop back correctly

            # concatenating encrypted character to encrypted message
            # chr() converts ascii value to character, which is why ascii_diff is added
            encrypted_msg += chr(encrypted_val + ascii_diff)

    return encrypted_msg

# decryption works the same as encryption, except key value is subtracted not added
def caesar_decrypt(encrypted_msg, key, special_case=True,
                    alphabet_size=26, upper_case=True):
    decrypted_msg = ""

    if upper_case:
        ascii_diff = ord('A')
    else:
        ascii_diff = ord('a')

    for x in encrypted_msg:
        if not isalpha(x) & special_case == True:
            decrypted_msg += x
        else:
            val = ord(x) - ascii_diff
            decrypted_val = (val - key) % alphabet_size

            decrypted_msg += chr(decrypted_val + ascii_diff)

    return decrypted_msg

# example
print(caesar_encrypt("TESTING", 7))
print(caesar_decrypt("ALZAPUN",7))
