from datetime import datetime
import os

from prefect import Flow

import config
import task

def get_dating_value(tick, delta, format):
    i, unit = delta.split()
    if unit == "M":
        return datetime.fromtimestamp(tick + int(i) * 60).strftime(format)
    if unit == "H":
        return datetime.fromtimestamp(tick + int(i) * 60 * 60).strftime(format)
    if unit == "d":
        return datetime.fromtimestamp(tick + int(i) * 60 * 60 * 24).strftime(format)
    if unit == "m":
        now = datetime.fromtimestamp(tick)
        div, mod = divmod(now.month + int(i), 12)
        if not mod:
            return now.replace(year=now.year + div - 1, month=12).strftime(format)
        return now.replace(year=now.year + div, month=mod).strftime(format)
    if unit == "Y":
        now = datetime.fromtimestamp(tick)
        return now.replace(year=now.year + int(i)).strftime(format)

def update_fetch_info(fetch_info, tick):
    dating = fetch_info["dating"]
    if dating:
    	for i, d in [("param", "delta"), ("end_param", "end_delta")]:
        	fetch_info["params"][dating[i]] = get_dating_value(tick, dating[d], dating["format"])
    return fetch_info

def update_store_info(store_info, _id, tick):
    run = datetime.fromtimestamp(tick).strftime("%Y%m%d%H%M%S")
    store_info["file"] = os.path.join(config.file_path, f"{_id}_{run}.csv")
    return store_info

def run(info, _id, tick):
    fetch_info = update_fetch_info(info["fetch"], tick)
    store_info = update_store_info(info["store"], _id, tick)
    with Flow(_id) as flow:
        items = task.fetch(fetch_info)
        task.store(store_info, items)
    result = flow.run()
    status = result.is_successful() and "succ" or "fail"
    return status, result.message

