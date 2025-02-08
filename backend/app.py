import fastapi
import asyncio
from backend import query
from backend import data_models
import os

app = fastapi.FastAPI()


@app.get("/connection")
async def connection():
    return {"status": "ok"}


@app.get("/deploy")
async def deploy():
    await asyncio.create_subprocess_shell("git pull origin main")
    return "deployed"


@app.post("/query/classroom")
async def query_classroom(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_classroom, cond.cond)
    return res
