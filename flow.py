from prefect import Flow, Parameter

import task

def run(_id, info):
    with Flow(_id) as flow:
        info_ = Parameter("info")
        items = task.extract(info_["extract"])
        task.load(info_["load"], items)
    result = flow.run(parameters=dict(info=info))
    status = result.is_successful() and "succ" or "fail"
    return status, result.message

if __name__ == "__main__":
    info = {
        "extract": {
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
        },
        "load": {
            "keys": ["baekduId", "baekdudistance", "baekdugbn", "baekdugbnname", "baekdurealdistance",
                     "baekdusectione", "baekdusections", "baekduspect", "baekduvia", "mntloca",
                     "mntnfile", "mntnnm"
            ],
            "file": "/home/sanxoo/ivi/file/20211125000001_ID.csv"
        },
    }
    status, message = run("ID", info)
    print(status, message)

