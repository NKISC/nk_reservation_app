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


@app.post("/query/record")
async def query_record(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_record, cond.cond)
    return res


@app.post("/query/display")
async def query_display(q: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_display, q.cond)
    return res


@app.post("/query/permission")
async def query_permission(q: data_models.PermissionCheckQuery):
    res = await asyncio.to_thread(query.check_permission, q.permissions, q.classrooms)
    return res
