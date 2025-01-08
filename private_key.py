from Crypto.PublicKey import RSA

# Generate RSA key pair
key = RSA.generate(2048)

# Save private key
with open("private_key.pem", "wb") as private_file:
    private_file.write(key.export_key())

# Save public key
with open("public_key.pem", "wb") as public_file:
    public_file.write(key.publickey().export_key())

print("Keys generated and saved as private_key.pem and public_key.pem")
