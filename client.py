import requests  #To send HTTP requests to the server. This is used to send the encrypted MAC address and salt to the server.
import uuid  
import os        # For generating random salt using os.urandom()
from Crypto.Cipher import AES  #The AES encryption method from the PyCryptodome library.
from Crypto.Util.Padding import pad  #Ensures that the plaintext is padded to fit AES block size (16 bytes).
from base64 import b64encode  #To encode the encrypted data and salt into base64 format so they can be safely transmitted over HTTP.

# Secret key (same as on the server, should be securely shared)
SECRET_KEY = b'mysecretkey12345'  #This is a 16-byte secret key used for AES encryption and decryption (AES-128).


# ************************************* Note : This is Symmetric Cryptography *************************************
# -------The key needs to be securely shared between the client and server so both can use the same key for encryption and decryption.------

# _____________________________________________________________________________________________________________________________________________________________________


# Function to get MAC address
def get_mac_address():

    # ******** This function formats the MAC address into a standard hexadecimal string, such as "00:14:22:01:23:45", using bitwise operations.**********
    # Get the MAC address of the system
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])  #uuid.getnode() retrieves the MAC address of the local machine (as a unique identifier).
    return mac
# _____________________________________________________________________________________________________________________________________________________________________

# Function to encrypt the MAC address using AES with salt
def encrypt_payload(data):
    # ********Salt Generation*********
    salt = os.urandom(16)  #A random salt of 16 bytes is generated 
    

    # Initialize AES cipher with the secret key and salt as IV
    # AES.new() method is used to create a new AES cipher object. The SECRET_KEY is used for encryption, and the salt is used as the Initialization Vector (IV) in CBC mode.

    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=salt)  # SECRET_KEY: This is a cryptographic key used to perform encryption and decryption in the AES algorithm. It's a secret value that must be kept secure. 
                                                         # The salt is used as the Initialization Vector (IV) in CBC mode.       
    # ******** Padding *********
                                                         #  An IV is a random or pseudo-random value used to ensure that identical plaintexts encrypt to different ciphertexts. In certain encryption modes, such as CBC, the IV is used in combination with the secret key to encrypt the data securely. Without an IV, the same plaintext encrypted multiple times would always result in the same ciphertext, making it vulnerable to cryptanalysis.          
    data_bytes = data.encode('utf-8')  #The MAC address is first converted to bytes using encode('utf-8')
    padded_data = pad(data_bytes, AES.block_size)  #pad() ensures the data's length is a multiple of the AES block size (16 bytes).
    
    # ******** Encrypt the data ******** 
    encrypted_data = cipher.encrypt(padded_data)
    
    # ******** Base64 Encoding  ********
    # Return the encrypted data along with the salt, both base64 encoded
    encrypted_data_b64 = b64encode(encrypted_data).decode('utf-8')
    salt_b64 = b64encode(salt).decode('utf-8')

# |-------------------------------------------------------------------------------------------------------------------------# |
# | The encrypted MAC address and salt are both encoded using base64 so they can be safely transmitted as text over HTTP.   # |
# |-------------------------------------------------------------------------------------------------------------------------# |
    return encrypted_data_b64, salt_b64

# Get MAC address
mac_address = get_mac_address()

# Encrypt the MAC address
encrypted_mac, salt = encrypt_payload(mac_address)

# API endpoint URL
#A POST request is sent to the server at http://127.0.0.1:5000/decrypt-mac with the encrypted MAC address and the salt (both base64-encoded).

url = 'http://127.0.0.1:5000/decrypt-mac' 
# Send encrypted MAC address and salt to the API
response = requests.post(url, json={"encrypted_mac": encrypted_mac, "salt": salt})

# Print the response from the server
print(response.json())
