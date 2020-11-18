# script for output hashed lines
# take any line in input, then hashed it in different mechanics without addition any alter keys.

import hashlib
#  input non hashing line
input_line = input("Enter string to hash:").encode()
# this line is reference from xml file. Field
hash_line_sha1 = "Op8ZGFBuNYAvEZAdAD+bUSysA54="
# outline_dict is store with diff types of hashes and reference input values
outline_dict = {
                "INPUT LINE": input_line,
                "REFERENCE HASH": hash_line_sha1,
                "MD5": hashlib.md5(input_line).hexdigest(),
                "SHA1": hashlib.sha1(input_line).hexdigest(),
                "SHA224": hashlib.sha224(input_line).hexdigest(),
                "SHA256": hashlib.sha256(input_line).hexdigest(),
                "SHA384": hashlib.sha384(input_line).hexdigest(),
                "SHA512": hashlib.sha512(input_line).hexdigest(),
                }

#  output types and hash lines
for key, value in outline_dict.items():
    print('{k:<15}: {val}'.format(k=key, val=value))