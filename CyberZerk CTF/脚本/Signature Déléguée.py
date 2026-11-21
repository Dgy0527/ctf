import base64, json

token = "eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VyIjogIm1hcmNfdiIsICJyb2xlIjogInVzZXIifQ.tzR6..."

header, payload, sig = token.split('.')
for name, seg in [("header", header), ("payload", payload)]:
    seg += '=' * (-len(seg) % 4)          # 补齐 Base64 的 =
    data = base64.urlsafe_b64decode(seg)  # URL 安全的 Base64
    print(name, json.loads(data))
