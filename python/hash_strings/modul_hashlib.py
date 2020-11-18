# script for output hashed lines
# take any line in input, then hashed it in different mechanics without addition any alter keys.
import hashlib

input_line = input("Enter string to hash:").encode()
outline_dict = {
                "INPUT LINE": input_line,
                "MD5": hashlib.md5(input_line).hexdigest(),
                "SHA1": hashlib.sha1(input_line).hexdigest(),
                "SHA224": hashlib.sha224(input_line).hexdigest(),
                "SHA256": hashlib.sha256(input_line).hexdigest(),
                "SHA384": hashlib.sha384(input_line).hexdigest(),
                "SHA512": hashlib.sha512(input_line).hexdigest(),
                }

for key, value in outline_dict.items():
    print('{k:<15}: {val}'.format(k=key, val=value))
