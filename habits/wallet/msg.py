from solders.keypair import Keypair

b58_string = "vGXRbf75NN3JnC6FaDZDGRjrAXU45RuZk5d5R77qjbHynTwE3i6VdGFNqCFgPquwWKbFcnABVKFofQdzZZADvdZ"
keypair = Keypair.from_base58_string(b58_string)
print(keypair)
print("restored Keypair with Public Key: {}".format(keypair.pubkey()))

message = b"The quick brown fox jumps over the lazy dog"
signature = keypair.sign_message(message)
verify_sign = signature.verify(keypair.pubkey(), message); print(verify_sign) # bool

b = Keypair(); verify_sign = signature.verify(b.pubkey(), message); print(verify_sign) # bool
