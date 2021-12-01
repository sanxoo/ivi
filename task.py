import requests
import json
import xml.etree.ElementTree
import csv

from prefect import task

def parse_json_items(text, path):
	return []

def parse_json_value(text, path):
	return ""

def parse_xml_items(text, path):
    items = []
    for item in xml.etree.ElementTree.fromstring(text).iterfind(path):
        items.append({e.tag:e.text for e in item})
    return items

def parse_xml_value(text, path):
    return xml.etree.ElementTree.fromstring(text).find(path).text

parse_func = {
    "json": {
        "items": parse_json_items,
        "value": parse_json_value,
    },
    "xml": {
        "items": parse_xml_items,
        "value": parse_xml_value,
    },
}

def fetch_with_paging(info):
    params = info["params"].copy()
    params[info["paging"]["param"]] = info["paging"]["start_value"]
    res = requests.get(info["url"], params=params)
    items = parse_func[info["format"]]["items"](res.text, info["item_path"])
    total = parse_func[info["format"]]["value"](res.text, info["paging"]["total_count_path"])
    while len(items) < int(total):
        params[info["paging"]["param"]] += 1
        res = requests.get(info["url"], params=params)
        items += parse_func[info["format"]]["items"](res.text, info["item_path"])
    return items

def fetch_without_paging(info):
    res = requests.get(info["url"], params=info["params"])
    items = parse_func[info["format"]]["items"](res.text, info["item_path"])
    return items

@task
def fetch(info):
    return fetch_with_paging(info) if info.get("paging") else fetch_without_paging(info)

@task
def store(info, items):
    with open(info["file"], "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(info["keys"])
        for item in items:
            row = [item[key] for key in info["keys"]]
            writer.writerow(row)
        
if __name__ == "__main__":
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
    items = fetch.run(info["fetch"])
    store.run(info["store"], items)

