from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

# Tạo key pair RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Chuyển đổi key pair sang định dạng PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# In key pair và định dạng PEM
print("Private key:")
print(private_pem.decode('utf-8'))
print("Public key:")
print(public_pem.decode('utf-8'))

# Mã hóa và giải mã thông điệp
message = b"Nhung"

# Mã hóa bằng public key
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hash.SHA256()),
        algorithm=hash.SHA256(),
        label=None
    )
)

# Giải mã bằng private key
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hash.SHA256()),
        algorithm=hash.SHA256(),
        label=None
    )
)
# In thông điệp đã giải mã
print("Plaintext:", plaintext.decode('utf-8'))
