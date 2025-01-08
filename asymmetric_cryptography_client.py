#(Encryption with Public Key)

import requests
import uuid
import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
# _____________________________________________________________________________________________________________________________________________________________________

# Load public key
with open("public_key.pem", "rb") as public_file:
    public_key = RSA.import_key(public_file.read())

# _____________________________________________________________________________________________________________________________________________________________________
# Function to get MAC address
def get_mac_address():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])

# _____________________________________________________________________________________________________________________________________________________________________ 
# Function to generate a random salt
def generate_salt():
    return os.urandom(16)  # Generate 16-byte random salt

# _____________________________________________________________________________________________________________________________________________________________________

# Function to encrypt MAC address with salt
def encrypt_payload_with_salt(data, salt):
    combined_data = f"{salt.hex()}:{data}"  # Combine salt and data
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(combined_data.encode('utf-8'))
    return b64encode(encrypted_data).decode('utf-8')

# _____________________________________________________________________________________________________________________________________________________________________

# API endpoint URL
url = 'http://127.0.0.1:5000/decrypt-mac'

# _____________________________________________________________________________________________________________________________________________________________________

# Get MAC address
mac_address = get_mac_address()
print(f"[Client] Original MAC Address: {mac_address}\n ")

# _____________________________________________________________________________________________________________________________________________________________________

# Encrypt and send the MAC address three times
for i in range(3):
    salt = generate_salt()
    encrypted_mac = encrypt_payload_with_salt(mac_address, salt)
    print(f"[Client] Encrypted MAC Address {i+1}: {encrypted_mac}\n ")
    
    # Send the encrypted MAC address to the API
    response = requests.post(url, json={"encrypted_mac": encrypted_mac})
    print(f"[Client] Server Response {i+1}: {response.json()}\n ")
