from datetime import datetime

import sida
import task
import jobs

def test(info):
    tick = datetime.today().timestamp()
    info = sida.inject_dating_params(info, tick)
    return task.extract.run(info)

def lst():
    return jobs.select()

def create(data):
    jobs.insert(**data)
    return get(data["_id"])

def get(_id):
    return jobs.select(_id)[0]

def update(_id, data):
    jobs.update(_id, **data)
    return get(_id)

def delete(_id):
    jobs.delete(_id)

def log(_id):
    return jobs.logs.select(_id=_id)

if __name__ == "__main__":
    import json
    import uuid
    info, _id, tick = json.load(open("info.json")), str(uuid.uuid4()), datetime.today().timestamp()

    for item in test(info["extract"]): print(item)

    """
    for job in lst():
        print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")

    data = {
        "_id": t_id,
        "name": "corona occurrence status",
        "info": json.dumps(info),
        "schedule": "0 1 * * *",
    }
    job = create(data)
    print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")
    print(f"{job['info']}")

    job = update(t_id, {"schedule": "1 1 * * *", "last_run": "20211128183000"})
    print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")
    print(f"{job['info']}")

    delete(t_id)

    for job in lst():
        print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")
    """

