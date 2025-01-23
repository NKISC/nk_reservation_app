import fastapi
import os

app = fastapi.FastAPI()


@app.get("/connection")
async def connection():
    return {"status": "ok"}

@app.get("/deploy")
async def deploy():
    os.system("git pull origin main")
    return "deployed"
