from flask import Flask, request, jsonify #used to create the API endpoint that will accept requests from the client.
from Crypto.Cipher import AES #AES decryption method from the PyCryptodome library.
from Crypto.Util.Padding import unpad # To remove padding from the decrypted data.
from base64 import b64decode # To decode the base64 encoded data.

app = Flask(__name__)

# Secret key used for encryption and decryption (same as in client)
SECRET_KEY = b'mysecretkey12345'  # 16 bytes for AES-128

# |------------------------------------------------------------------------------------------------------------------------------------------------# |
# | This is the same 16-byte secret key used by the client for encryption. It must match the key used on the client side for successful decryption.# |
# |------------------------------------------------------------------------------------------------------------------------------------------------# |

# Function to decrypt the MAC address using salt
def decrypt_payload(encrypted_payload, salt):
    # The encrypted_payload and salt are decoded from base64 back into their original byte forms.    encrypted_data = b64decode(encrypted_payload) 
    encrypted_data = b64decode(encrypted_payload)    
    salt = b64decode(salt)
    
    # Initialize AES cipher with the secret key and salt as IV
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=salt)  # Salt used as IV
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)  

    print(f"[Server] Encrypted MAC Address (Base64): {encrypted_payload}\n ")
    print(f"[Server] Salt (Base64): {salt.hex()}\n ")
    print(f"[Server] Decrypted MAC Address: {decrypted_data.decode('utf-8')}\n ") 

    return decrypted_data.decode('utf-8') #After decryption, the result is decoded back into a UTF-8 string (which should be the original MAC address).

@app.route('/decrypt-mac', methods=['POST'])  #This decorator defines the API endpoint where the client sends the encrypted MAC address and the salt.
# The function handle_decrypted_mac() extracts the encrypted_mac and salt from the incoming JSON request.
def handle_decrypted_mac():
    encrypted_mac = request.json.get('encrypted_mac')
    salt = request.json.get('salt')

    #If both values are provided, it calls the decrypt_payload() function to decrypt the MAC address. 
    if encrypted_mac and salt:
        try:
            decrypted_mac = decrypt_payload(encrypted_mac, salt)
            return jsonify({'status': 'success', 'mac_address': decrypted_mac}), 200
        except Exception as e:
            print("[Server] Error during decryption:", str(e))        
            return jsonify({'status': 'error', 'message': 'Decryption failed'}), 400
    else:
        print("[Server] Error: Missing encrypted MAC or salt")
        return jsonify({'status': 'error', 'message': 'No encrypted MAC address or salt provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
