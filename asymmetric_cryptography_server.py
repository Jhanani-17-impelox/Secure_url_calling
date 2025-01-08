#(Decryption with Private Key)


from flask import Flask, request, jsonify
from Crypto.Cipher import PKCS1_OAEP   #PKCS1_OAEP is Used for decrypting the encrypted data.
from Crypto.PublicKey import RSA       #RSA is Used for decrypting the encrypted data.

from base64 import b64decode           #decode the encrypted data from Base64 format back into its binary form before decryption.

# _____________________________________________________________________________________________________________________________________________________________________
app = Flask(__name__)

# Load private key
with open("private_key.pem", "rb") as private_file:
    private_key = RSA.import_key(private_file.read())

# _____________________________________________________________________________________________________________________________________________________________________

# Decrypt payload
def decrypt_payload_with_salt(encrypted_data):
    cipher = PKCS1_OAEP.new(private_key)
    decoded_data = b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_data).decode('utf-8')
    
    # Extract salt and MAC address
    salt, mac_address = decrypted_data.split(":", 1)
    print(f"[Server] Extracted Salt: {salt}")
    return mac_address

# _____________________________________________________________________________________________________________________________________________________________________

@app.route('/decrypt-mac', methods=['POST'])
def decrypt_mac():
    data = request.json
    encrypted_mac = data.get("encrypted_mac")
    if not encrypted_mac:
        return jsonify({"status": "error", "message": "No encrypted_mac provided"}), 400

    try:
        # Decrypt MAC address with salt
        mac_address = decrypt_payload_with_salt(encrypted_mac)
        print(f"[Server] Decrypted MAC Address: {mac_address}\n ")
        return jsonify({"status": "success", "mac_address": mac_address})
    except Exception as e:
        print(f"[Server] Decryption failed: {e}\n ")
        return jsonify({"status": "error", "message": "Decryption failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
