import json
import hashlib

# db: dict = {}
#
# db ['admin'] = {"password": "", "count_hash_iteration": 20, "count_try_true": 1}
# filename = 'db.json'
# with open(f'{filename}', 'w') as write_file:
#     json.dump(db, write_file, indent=3)

# password = "admin"

# for i in range(19):
#     password = hashlib.pbkdf2_hmac('sha256', password.encode(), ''.encode(), 10000).hex()
#
# print(password)

# password = hashlib.pbkdf2_hmac('sha256', "fc43446527385ba0fb9c09c8dc1290109affdc914ca3cac4a54febae24c0d16c".encode(), ''.encode(), 10000).hex()
# print(password)
import time
def wait():
    for i in range(40):
        print("###", end="")
        time.sleep(0.1)
wait()
