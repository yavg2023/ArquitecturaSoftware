from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import time

app = FastAPI()
SECRET = "villamil"

users_db = {
    "alice": {"password": "1234", "subscription": "premium"},
    "bob": {"password": "abcd", "subscription": "basic"}
}

@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    payload = {
        "sub": form_data.username,
        "subscription": user["subscription"],
        "exp": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
