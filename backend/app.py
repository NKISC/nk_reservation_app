import fastapi
import os

app = fastapi.FastAPI()


@app.get("/deploy")
def deploy():
    os.system("git pull origin main")
    return "deployed"
