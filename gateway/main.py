from fastapi import FastAPI, Request, HTTPException
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()
SECRET = "villamil"

@app.middleware("http")
async def verify_token(request: Request, call_next):
    if request.url.path.startswith("/video"):
        auth = request.headers.get("Authorization")
        if not auth:
            return JSONResponse(status_code=401, content={"detail": "Token no proporcionado"})

        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            subscription = payload.get("subscription")

            if subscription != "premium":
                return JSONResponse(status_code=403, content={"detail": "Sin acceso a contenido premium"})

        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Token inválido"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": f"Error interno inesperado: {str(e)}"})

    return await call_next(request)


@app.get("/video")
async def proxy_video():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://video_service:8002/video")
            return response.json()
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error al contactar el servicio de video: {str(e)}"})