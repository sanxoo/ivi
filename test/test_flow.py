import sys; sys.path.append("..")

import json
from datetime import datetime

import flow

def test_update():
    info, _id, tick = json.load(open("info.json")), "_id", datetime.today().timestamp()
	print(info["fetch"])
    print(flow.update_fetch_info(info["fetch"], tick))
	print(info["store"])
    print(flow.update_store_info(info["store"], _id, tick))

def test_fetch():
    info, _id, tick = json.load(open("info.json")), "_id", datetime.today().timestamp()
	for item in flow.run_fetch(info["fetch"], tick):
		print(item)

def test_run():
    info, _id, tick = json.load(open("info.json")), "_id", datetime.today().timestamp()
    status, message = flow.run(info, _id, tick)
    print(status, message)

if __name__ == "__main__":
    test_update()
    test_run()

