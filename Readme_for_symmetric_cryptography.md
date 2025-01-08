# Secure API with Payload Encryption Using Salt

This project demonstrates how to securely send sensitive data (e.g., the MAC address of a system) to an API by encrypting the payload with **AES encryption** and using a **random salt** to ensure that even the same plaintext input produces different ciphertext each time.

## Features
- **Encryption with Salt**: Each encryption process uses a random salt to ensure unique ciphertexts for identical plaintexts.
- **Secure API Communication**: Encrypted data is transmitted to the API along with the salt.
- **Decryption on the Server**: The API decrypts the payload using the provided salt and retrieves the original plaintext.

---

## Requirements
To run this project, ensure you have Python installed and the following libraries:

- Flask
- PyCryptodome
- Requests

### Install Dependencies
Run the following command to install the required libraries:
```bash
pip install flask pycryptodome requests
```

---

## Project Structure
```
.
├── client.py  # Client script to encrypt data and send it to the API
├── server.py  # API to decrypt the received payload
└── README.md  # Documentation
```

---

## How It Works

### Encryption (Client Side)
1. The **MAC address** of the system is retrieved.
2. A **random salt** is generated for each encryption.
3. The MAC address is encrypted using AES with the salt as the **Initialization Vector (IV)**.
4. The encrypted data and salt are sent to the API.

### Decryption (Server Side)
1. The API receives the encrypted data and the salt.
2. Using the salt as the IV, the server decrypts the data with the same AES key.
3. The original plaintext (MAC address) is returned in the response.

---

## Running the Project

### Step 1: Run the API (Server)
Start the server by running the `server.py` file:
```bash
python server.py
```
This will start the API on `http://127.0.0.1:5000`.

### Step 2: Run the Client
Run the `client.py` file to retrieve the MAC address, encrypt it, and send it to the API:
```bash
python client.py
```
The client will display the decrypted MAC address returned by the API.

---

## Example Workflow
1. **Client**:
   - MAC Address: `00:1a:2b:3c:4d:5e`
   - Encrypted Data: (Random each time)
   - Salt: (Random each time)

2. **API Response**:
   ```json
   {
       "status": "success",
       "mac_address": "00:1a:2b:3c:4d:5e"
   }
   ```

----