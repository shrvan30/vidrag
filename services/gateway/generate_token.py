from jose import jwt

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

payload = {"user": "shravan"}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(token)