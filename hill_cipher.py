import numpy as np
import math

def encrypt(plain_text,key_matrix):
    plain_text_words = plain_text.split(' ')
    cipher_text = []
    extras  = []

    for word in plain_text_words:
        cipher_text_word,extra = encrypt_word(word,key_matrix)
        cipher_text.append(cipher_text_word)
        extras.append(extra)
    
    return " ".join(cipher_text),extras

def decrypt(cipher_text,key_matrix,extras=None):
    cipher_text_words = cipher_text.split(' ')

    if(extras == None):
        extras = [0 for i in range(len(cipher_text_words))]

    plain_text = []
    for i in range(len(cipher_text_words)):
        plain_text.append(decrypt_word(cipher_text_words[i],key_matrix,extras[i]))
    
    return " ".join(plain_text)

def encrypt_word(plain_text,key_matrix,debug=False):
    key_matrix = np.array(key_matrix)
    key_dim = key_matrix.shape[0]
    dimensions = len(plain_text)

    extra = 0 # padding
    if(dimensions%key_dim != 0):
        extra = key_dim - dimensions%key_dim
    
    # creating a column matrix for plain text characters
    plain_text_matrix = []
    for i in range(dimensions):
        plain_text_matrix.append(ord(plain_text[i]) - 65)

    # pad 0s in the end
    for i in range(extra):
        plain_text_matrix.append(0)
    
    plain_text_matrix = np.array(plain_text_matrix)

    # encryption
    result = []
    index = 0
    for i in range(int((dimensions+extra)/key_dim)):
        result.append(np.dot(plain_text_matrix[index:index+key_dim],key_matrix))
        index += key_dim
    
    # converting result to cipher text
    cipher_text = ""
    for window in result:
        for num in window:
            cipher_text += chr(num % 26 + 65)
    
    if(debug):
        print("key dimensions: ",key_dim)
        print("length of plain text: ",plain_text)
        print("number of extra characters padded: ",extra)
        print("plain text matrix: ",plain_text_matrix)
        print("cipher text matrix: ",result)
        print("cipher text: ",cipher_text)
    
    return (cipher_text,extra)

# decryption function
def decrypt_word(cipher_text,key_matrix,extra=0,debug=False):
    key_matrix = np.array(key_matrix)
    key_dim = key_matrix.shape[0]
    key_matrix_inv = np.linalg.inv(key_matrix)
    dimensions = len(cipher_text)

    # create cipher text matrix (ASCII Values - 65 to get from 0 to X)
    cipher_text_matrix = []
    for i in range(dimensions):
        cipher_text_matrix.append(ord(cipher_text[i]) - 65)
    
    cipher_text_matrix = np.array(cipher_text_matrix)

    # multiply inverse with cipher text matrix
    result = []
    index = 0
    for i in range(int((dimensions)/key_dim)):
        result.append(np.dot(cipher_text_matrix[index:index+key_dim],key_matrix_inv))
        index += key_dim

    plain_text = ""
    for window in result:
        for num in window:
            plain_text += chr(int(round(num,0) % 26 + 65))
    
    # remove padding
    if(extra != 0):
        plain_text = plain_text[0:-extra]

    if(debug):
        print("key dimensions: ",key_dim)
        print("number of extra characters padded: ",extra)
        print("cipher text matrix: ",cipher_text_matrix)
        print("plain text matrix(with padding): ",result)
        print("plain text: ",plain_text)

    return plain_text

def check_key(key_matrix):
    key_matrix = np.array(key_matrix)
    if(key_matrix.shape[0] != key_matrix.shape[1]):
        return False

    det = np.linalg.det(key_matrix)

    if(det == 0 or det%2 == 0 or det%13 == 0):
        return False

    test_string = "TEST"
    cipher_text,extras = encrypt(test_string,key_matrix)
    plain_text = decrypt(cipher_text,key_matrix,extras)

    if(test_string != plain_text):
        return False
    
    return True

if __name__ == "__main__":
    # plain_text = str(input("Plain Text: "))
    key_matrix = np.array([[8,6,9,5],[6,9,5,10],[5,8,4,9],[10,6,11,4]])
    key_matrix2 = np.array([[1,1,1,-1],[1,1,-1,1],[1,-1,1,1],[-1,1,1,1]])
    key_matrix3 = np.array([[2,5,0,8],[1,4,2,6],[7,8,9,3],[1,5,7,8]])

    print(check_key(key_matrix))
    print(check_key(key_matrix2))
    print(check_key(key_matrix3))

    # cipher_text,extra = encrypt(plain_text,key_matrix)
    # print("cipher text: ",cipher_text)

    # plain_text = decrypt(cipher_text,key_matrix,extra)
    # print("plain text: ",plain_text)

