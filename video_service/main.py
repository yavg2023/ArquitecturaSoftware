from fastapi import FastAPI

app = FastAPI()

@app.get("/video")
def get_video():
    return {"message": "🎬 Este es el contenido premium. ¡Disfruta tu película!"}
