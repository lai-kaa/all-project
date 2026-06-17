import hmac, hashlib, time, os
def sign_payload(secret, payload, nonce=None):
 nonce = nonce or str(int(time.time()))
 msg = (payload + nonce).encode("utf-8")
 return nonce, hmac.new(secret.encode("utf-8"), msg,
hashlib.sha256).hexdigest()
payload = '{"q":"hello"}'
nonce, sig = sign_payload(os.getenv("CLIENT_SECRET",""), payload)
headers = {"X-Nonce": nonce, "X-Signature": sig}