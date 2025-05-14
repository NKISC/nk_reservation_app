import fastapi
import asyncio
import sqlite3
from backend import query
from backend import data_models
from backend import addition

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


@app.get("/img/{url}")
async def query_img(url: str):
    res = await asyncio.to_thread(query.query_img, url)
    return fastapi.Response(content=res, media_type="image/jpeg")


@app.post("/addition/add_record")
async def addition_record(q: data_models.RecordAdditionModel):
    res = await asyncio.to_thread(addition.add_records, q.classroom, q.noon, q.applicant_id, q.time_stamp)
    return res

@app.post("/addition/add_user")
async def addition_user(q: data_models.UserAdditionModel):
    res = await asyncio.to_thread(addition.add_user, q.display_name, q.permissions)
    return res