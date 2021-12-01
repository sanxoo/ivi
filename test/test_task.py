import sys; sys.path.append("..")

import task

def test_fetch_and_store():
    info = {
        "fetch": {
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
        "store": {
            "keys": ["baekduId", "baekdudistance", "baekdugbn", "baekdugbnname", "baekdurealdistance",
                     "baekdusectione", "baekdusections", "baekduspect", "baekduvia", "mntloca",
                     "mntnfile", "mntnnm"
            ],
            "file": "/home/sanxoo/ivi/file/task.csv"
        },
    }
    items = task.fetch.run(info["fetch"])
    task.store.run(info["store"], items)

if __name__ == "__main__":
    test_fetch_and_store()

