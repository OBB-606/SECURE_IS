import hashlib
password = "1234"
role = 'admin'

print(hashlib.pbkdf2_hmac('sha256', password.encode(), role.encode(), 100000).hex())