import task

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
items = task.extract.run(info)
for item in items:
    print(item)

