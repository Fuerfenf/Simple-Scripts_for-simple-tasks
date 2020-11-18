# script - example of hashing with add alter keys in input data logic and
# logic for compared store hash and input pass hash
# hashing in sha256 as example

import uuid
import hashlib


#  fn for hashing input value
def hash_password(password):
    # uuid generate random number -> salt
    salt = uuid.uuid4().hex
    # returned hash value after concatenation: salt_hash + pass_hash + salt_hash
    # this way as example and it can be changed in diff situations and developer approach
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


#  fn for check passwords sames or no by hash
def check_password(hashed_password, user_password):
    #  this split store hashed pass by : and save in password hashed pass (part is: salt_hash + pass_hash)
    #  in salt saved salt_hash
    password, salt = hashed_password.split(':')
    # if hashes sames return true else return false
    # hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() this is get hash from second input
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


input_pass = input('input pass for hash and save in store: ')
hashed_password = hash_password(input_pass)
used_pass = input('Input pass for checking it: ')
output = 'Input correct pass' if check_password(hashed_password, used_pass) else "Wrong pass"
print(output)
