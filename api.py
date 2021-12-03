import os
import logging.handlers
import logging
from datetime import datetime

from fastapi import FastAPI, Request

import config
import jobs
import flow
import task

api = FastAPI()

@api.get("/jobs", status_code=200)
async def lst():
    return jobs.select()

@api.get("/jobs/{_id}", status_code=200)
async def get(_id: str):
    return jobs.select(_id)[0]

@api.get("/jobs/{_id}/logs", status_code=200)
async def log(_id: str):
    jobs.logs.select(_id=_id)

@api.post("/jobs", status_code=201)
async def create(request: Request):
    data = await request.json()
    jobs.insert(**data)
    return await get(data["_id"])

@api.patch("/jobs/{_id}", status_code=200)
async def update(_id: str, request: Request):
    data = await request.json()
    jobs.update(_id, **data)
    return await get(_id)

@api.delete("/jobs/{_id}", status_code=204)
async def delete(_id: str):
    jobs.delete(_id)

@api.post("/test", status_code=200)
async def test(request: Request):
    data = await request.json()
    tick = datetime.today().timestamp()
    info = flow.uodate_fetch_info(data, tick)
    return task.fetch.run(info)

if __name__ == "__main__":
    logfile = os.path.join(config.logs_path, "api.log")
    handler = logging.handlers.RotatingFileHandler(logfile, "a", 10 * 1024 * 1024, 9)
    handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s:%(lineno)3d : %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8080)

