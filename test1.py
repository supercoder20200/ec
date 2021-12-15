import ecdsa
import hashlib
import base58

def bytes_to_hex_string(b: bytes):
    return ''.join('{:02x}'.format(x) for x in b).upper()

def get_prepend_if_even_or_odd_for_compressed(x_point):
    y = int(x_point[64:], 16)
    if y % 1 == 1:
        return "03"  # odd
    return "02"  # even

private_key = "e41b45e722251672c01a28e4fada590471fea09f90d13b143033ed3a1107ef49"

# Convert hex private key to bytes
private_key = bytes.fromhex(private_key)
print( "Private key hex string: {}".format( bytes_to_hex_string(private_key)))
#print(f"Private key bytes: \t\t\t {private_key}")
# Derivation of the private key
signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

verifying_key = signing_key.get_verifying_key()
#print(f"Verifying key, x and y points (bytes):\t{verifying_key.to_string()}", type(verifying_key.to_string()))

x_point = bytes_to_hex_string(verifying_key.to_string())
print(f"Uncompressed private key (hex):\t\t 04{x_point.upper()}")

even_odd = get_prepend_if_even_or_odd_for_compressed(x_point)
print(f"Compressed private key in (hex):\t {even_odd}{x_point.upper()[:64]}")

# public_key = bytes.fromhex("04") + verifying_key.to_string()  # this is error, you're using uncompressed private key
public_key = bytes.fromhex(even_odd) + verifying_key.to_string()[:32]

# Hashes of public key
sha256_1 = hashlib.sha256(public_key)  # now public_key contains compressed private key
ripemd160 = hashlib.new("ripemd160")
ripemd160.update(sha256_1.digest())

# Adding prefix to identify Network
hashed_public_key = bytes.fromhex("00") + ripemd160.digest() # hashed_private_key is public key

# Checksum calculation
checksum_full = hashlib.sha256(
    hashlib.sha256(hashed_public_key).digest()).digest()
checksum = checksum_full[:4]

# Adding checksum to hashpubkey
bin_addr = hashed_public_key + checksum

# Encoding to address
address = str(base58.b58encode(bin_addr))
final_address = address[2:-1]  # change 2

print(f"Public compressed key (hex): \t\t {final_address}")