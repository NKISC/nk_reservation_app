import fastapi
import asyncio
import os

app = fastapi.FastAPI()


@app.get("/connection")
async def connection():
    return {"status": "ok"}

@app.get("/deploy")
async def deploy():
    await asyncio.create_subprocess_shell("git pull origin master")
    return "deployed"
