import fastapi
import asyncio
import sqlite3
from backend import query
from backend import data_models
from backend import addition
from backend import utils
from backend import alter
from backend import deletion

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


@app.post("/addition/add_cyclical_record")
async def add_cyclical_record(q: data_models.CyclicalRecordAdditionModel):
    res = await asyncio.to_thread(addition.add_cyclical_records, q.classroom, q.noon,
                                  q.applicant_id, q.beginning_time_stamp, q.ending_time_stamp, q.days)
    return res


@app.post("/query/user")
async def query_user(q: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.query_user, q.cond)
    return res

  
@app.post("/addition/add_user")
async def addition_user(q: data_models.UserAdditionModel):
    res = await asyncio.to_thread(addition.add_user, q.display_name, q.permissions)
    return res


@app.get("/query/func_tags")
async def query_func_tags():
    res = await asyncio.to_thread(query.get_all_func_tags)
    return res


@app.post("/login/")
async def handle_login(login_model: data_models.LoginModel):
    res = await asyncio.to_thread(utils.login, login_model.code)
    return res


@app.post("/grant_access/")
async def grant_access(grant_access_req: data_models.GrantAccessModel):
    res = await asyncio.to_thread(utils.grant_access_from_password,
                                  grant_access_req.uid, grant_access_req.display, grant_access_req.password)
    return res


@app.post("/alter/user/")
async def alter_user(alter_req: data_models.UserAlterModel):
    res = await asyncio.to_thread(alter.alter_user, alter_req.uid, alter_req.display, alter_req.permission)
    return res


@app.post("/delete/record/")
async def delete_record(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(deletion.delete_record, cond.cond)
    return res


@app.post("/delete/classroom/")
async def delete_classroom(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(deletion.delete_classroom, cond.cond)
    return res


@app.post("/delete/user/")
async def delete_user(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(deletion.delete_user, cond.cond)
    return res


@app.post("/alter/record")
async def alter_record(alter_req: data_models.RecordAlterModel):
    res = await asyncio.to_thread(alter.alter_record, alter_req.record_id, alter_req.noon, alter_req.time_stamp)
    return res

@app.post("/query/cyclical")
async def get_cyclical(cond: data_models.BasePostQuery):
    res = await asyncio.to_thread(query.get_cyclical, cond.cond)
    return res


@app.post("/delete/cyclical/")
async def delete_cyclical(q: data_models.CyclicalDeletionModel):
    res = await asyncio.to_thread(deletion.delete_cyclical, q.initiator)
    return res


@app.get("/query/generate_schedule/")
async def generate_schedule():
    res = await asyncio.to_thread(query.generate_schedule)
    return res


@app.get("/query/schedule/")
async def get_schedule():
    return fastapi.responses.FileResponse("schedule.xlsx", filename="schedule.xlsx")


@app.get("/query/generate_statistics/")
async def generate_statistics():
    res = await asyncio.to_thread(query.generate_statistics)
    return res


@app.get("/query/statistics/")
async def get_statistics():
    with open(f"statistics.png", "rb") as img_file:
        img = img_file.read()
    return fastapi.Response(content=img, media_type="image/png")


@app.get("/query/ppm")
async def get_ppm():
    return query.get_permission_passwords()


@app.post("/addition/ppm/")
async def add_ppm(cond: data_models.BasePostQuery):
    return await asyncio.to_thread(addition.add_permission_password,
                                   cond.cond["password"], cond.cond["permission"], cond.cond["isDisposable"])


@app.post("/delete/ppm/")
async def delete_ppm(cond: data_models.BasePostQuery):
    return await asyncio.to_thread(deletion.delete_permission_password, cond.cond["password"])
