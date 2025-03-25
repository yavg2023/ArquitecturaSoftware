from fastapi import FastAPI, Request, HTTPException
from jose import jwt, JWTError

app = FastAPI()
SECRET = "villamil"

@app.middleware("http")
async def verify_token(request: Request, call_next):
    if request.url.path.startswith("/video"):
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Token no proporcionado")

        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            subscription = payload.get("subscription")

            if subscription != "premium":
                raise HTTPException(status_code=403, detail="Sin acceso a contenido premium")

        except HTTPException as e:
            raise e  # Deja pasar errores ya controlados (401, 403)
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
        except Exception:
            raise HTTPException(status_code=500, detail="Error interno inesperado")

    return await call_next(request)

@app.get("/video")
async def proxy_video():
    return {"message": "Proxy funcionando (pero este endpoint no debe usarse directamente)"}
