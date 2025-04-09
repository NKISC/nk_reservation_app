import fastapi
import asyncio
import sqlite3
from backend import query
from backend import data_models

app = fastapi.FastAPI()
db = sqlite3.connect('database.db')


@app.get("/connection")
async def connection():
    return {"status": "ok"}


@app.get("/deploy")
async def deploy():
    await asyncio.create_subprocess_shell("git pull origin main")
    return "deployed"


@app.post("/query/classroom")
async def query_classroom(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_classroom, db, cond.cond)
    return res


@app.post("/query/record")
async def query_record(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_record, db, cond.cond)
    return res


@app.post("/query/display")
async def query_display(q: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_display, db, q.cond)
    return res


@app.post("/query/permission")
async def query_permission(q: data_models.PermissionCheckQuery):
    res = await asyncio.to_thread(query.check_permission, db, q.permissions, q.classrooms)
    return res


@app.get("/img/{url}")
async def query_img(url: str):
    res = await asyncio.to_thread(query.query_img, url)
    return fastapi.Response(content=res, media_type="image/jpeg")
