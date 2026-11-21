import base64, hmac, hashlib, json, urllib.request

B = "https://signature-deleguee.cyberzerk.fr"
pub = urllib.request.urlopen(B + "/pubkey", timeout=15).read()

def b64(d):
    return base64.urlsafe_b64encode(d).rstrip(b'=')

header  = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
payload = b64(json.dumps({"user": "marc_v", "role": "admin"}).encode())
signing = header + b'.' + payload
sig     = hmac.new(pub, signing, hashlib.sha256).digest()
token   = (signing + b'.' + b64(sig)).decode()

req = urllib.request.Request(B + "/admin", headers={"Authorization": "Bearer " + token})
print(urllib.request.urlopen(req, timeout=15).read().decode())
