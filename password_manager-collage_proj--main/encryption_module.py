from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import string
import base64
import csv
import os

def encrypt_password(user, service, key, password):
    # Pad the key to 16 bytes (128 bits) for AES encryption
    key = key.ljust(16, '\x00').encode('utf-8')
    
    # Encode the password strings as bytes
    password_bytes = password.encode('utf-8')

    #padding the password into 16 btyes boundary
    password_bytes = pad(password_bytes, 16)
    
    # Generate a new 16-byte initialization vector (IV)
    iv = AES.new(key, AES.MODE_CBC).iv
    
    # Use the key and IV to encrypt the password using AES encryption in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_password = cipher.encrypt(password_bytes)
    
    #checking if the file exist
    file_path = f'password_manager-collage_proj--main\\password_manager-collage_proj--main\\data\\user_data\\{user}.csv'
    if os.path.isfile(file_path) == False:
        with open(file_path, mode='w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['service','iv','password'])
        
    with open(file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([service, iv.hex(), encrypted_password.hex()]) 
        
def decrypt(key, iv, encrypted_password):
    
    # converting bacck to bytes
    iv =bytes.fromhex(iv)
    encrypted_password =bytes.fromhex(encrypted_password)
    key =key.ljust(16,'\x00').encode('UTF-8')   
    
    # using key to decrypt the password encrypted in AES encryption in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_password_bytes = cipher.decrypt(encrypted_password)
    decrypted_password = unpad(decrypted_password_bytes, 16).decode('utf-8').replace('\x0e', '')
    
    return decrypted_password


# Generate password
def generate_password(length=18):
    # Defining characters used for making the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    integers = string.digits
    special_symb = string.punctuation
    
    # Combining every set
    all_set = lowercase + uppercase + integers + special_symb
    
    # Generating the random password
    random_bytes = get_random_bytes(length)
    password = ''
    for i in random_bytes:
        password += all_set[i % len(all_set)]
    
    return password

# Update password entry
def update_password(file_path, index, passkey, new_password):
        
        # Getting the new iv and encoding key 
        key = passkey.ljust(16,'\x00').encode('utf-8')
        new_iv = AES.new(key, AES.MODE_CBC).iv
        password_bytes = new_password.encode('utf-8')
        password_bytes = pad(password_bytes, 16)
        cipher = AES.new(key, AES.MODE_CBC, new_iv)
        new_encrypt_password = cipher.encrypt(password_bytes)
        
        # user file open to access content
        with open(file_path, mode='r', newline='') as csvfile:
            read = csv.reader(csvfile)
            reader = list(read)
        
        # Replacing old iv and password with new ones    
        for i, row in enumerate(reader):
            if i == (index + 1):
                row[1] = new_iv.hex()
                row[2] = new_encrypt_password.hex()
        
        # Rewriting the update content back in the file
        with open(file_path, mode='w',newline='') as csvfile:
            write = csv.writer(csvfile)
            write.writerows(reader)
