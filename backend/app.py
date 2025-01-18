import fastapi
import os

app = fastapi.FastAPI()


@app.get("/connection")
def connection():
    return {"status": "ok"}

@app.get("/deploy")
def deploy():
    os.system("git pull origin main")
    return "deployed"
