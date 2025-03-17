# Code for vigenere cipher tool
# Every character in the message is offset by its corresponding character in the key
from curses.ascii import isalpha


# alphabet_size is for alphabets that don't use every latin character, such as the Italian alphabet
# special_case determines if characters not in the latin alphabet are included

def vigenere_encrypt(msg, key, alphabet_size = 26,
                     upper_case = True, special_case = True):

    encrypted_msg = ""
    index = 0 # tracks current character in key

    # checking if ascii_diff should be for upper or lower case
    if upper_case:
        ascii_diff = ord('A')
    else:
        ascii_diff = ord('a')

    for x in msg:
        # checking for special characters and spaces
        if not isalpha(x) & special_case == True:
            encrypted_msg += x
        else:

            val_1 = ord(x) - ascii_diff
            val_2 = ord(key[index % len(key)]) - ascii_diff
            # index mod len(key) will ensure the key is looped through correctly

            encrypted_val = (val_1 + val_2) % alphabet_size
            # mod alphabet size ensures ascii values loop back correctly

            # concatenating encrypted character to encrypted message
            # chr() converts ascii value to character, which is why ascii_diff is added
            encrypted_msg += chr(encrypted_val + ascii_diff)

            index += 1

    return encrypted_msg

# decryption works the same as encryption, except ascii value of key is subtracted from msg
def vigenere_decrypt(encrypted_msg, key, alphabet_size = 26,
                     upper_case = True, special_case = True):

    decrypted_msg = " "
    index = 0

    if upper_case:
        ascii_diff = ord('A')
    else:
        ascii_diff = ord('a')

    for x in encrypted_msg:
        if not isalpha(x) & special_case == True:
            decrypted_msg += x
        else:
            val_1 = ord(x) - ascii_diff
            val_2 = ord(key[index % len(key)]) - ascii_diff

            decrypted_val = (val_1 - val_2) % alphabet_size # ascii values subtracted

            decrypted_msg += chr(decrypted_val + ascii_diff)

            index += 1

    return decrypted_msg

# example of the cipher

result = vigenere_encrypt("I LOOVE PEANUTS","BANANA")
decrypt = vigenere_decrypt(result, "BANANA")
print(result + "   " + decrypt)







