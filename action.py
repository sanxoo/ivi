import task
import jobs

def test(info):
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

if __name__ == "__main__":
    import uuid
    import json
    """
    info = {
        "url": "http://openapi.forest.go.kr/openapi/service/trailInfoService/gettrailservice",
        "params": {
            "ServiceKey": "NMXz8csGsBU0z3xf7Ut54KCV2anBkNSiWDLqnkb+L6apfHxoAoXYbz0jPNT/f9VX3R0ziEw/V2xhrosuOi2srw==",
        },
        "paging": {
            "param": "pageNo",
            "start_value": 1,
            "count_param": "numOfRows",
            "count_value": 5,
            "total_count_path": "body/totalCount",
        },
        "format": "xml",
        "item_path": "body/items/item",
    }
    for item in test(info): print(item)
    """

    for job in lst():
        print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")

    t_id = str(uuid.uuid4())
    info = {
        "extract": {
            "url": "http://openapi.forest.go.kr/openapi/service/trailInfoService/gettrailservice",
            "params": {
                "ServiceKey": "NMXz8csGsBU0z3xf7Ut54KCV2anBkNSiWDLqnkb+L6apfHxoAoXYbz0jPNT/f9VX3R0ziEw/V2xhrosuOi2srw==",
            },
            "dating": {
            },
            "paging": {
                "param": "pageNo",
                "start_value": 1,
                "count_param": "numOfRows",
                "count_value": 5,
                "total_count_path": "body/totalCount",
            },
            "format": "xml",
            "item_path": "body/items/item",
        },
        "load": {
            "keys": ["baekduId", "baekdudistance", "baekdugbn", "baekdugbnname", "baekdurealdistance",
                     "baekdusectione", "baekdusections", "baekduspect", "baekduvia", "mntloca",
                     "mntnfile", "mntnnm"
            ],
            "file": ""
        },
    }
    data = {
        "_id": t_id,
        "name": "forest trail info",
        "info": json.dumps(info),
        "schedule": "0 0 * * *",
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

