from datetime import datetime
import os

import config

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

def inject_dating_params(info, tick):
    dating = info["dating"]
    if not dating: return info
    for i, d in [("param", "delta"), ("end_param", "end_delta")]:
        info["params"][dating[i]] = get_dating_value(tick, dating[d], dating["format"])
    return info

def update_file(info, _id, tick):
    now = datetime.fromtimestamp(tick).strftime("%Y%m%d%H%M%S")
    info["file"] = os.path.join(config.file_path, f"{_id}_{now}.csv")
    return info

def update(info, _id, tick):
    info["fetch"] = inject_dating_params(info["fetch"], tick)
    info["store"] = update_file(info["store"], _id, tick)
    return info

if __name__ == "__main__":
    import json
    info, _id, tick = json.load(open("info.json")), "_id", datetime.today().timestamp()

    # print(get_dating_value(tick, "-5 M", "%Y%m%d%H%M%S"))
    # print(get_dating_value(tick, "-6 H", "%Y%m%d%H%M%S"))
    # print(get_dating_value(tick, "-1 d", "%Y%m%d%H%M%S"))
    # print(get_dating_value(tick, "-1 m", "%Y%m%d%H%M%S"))
    # print(get_dating_value(tick, "-1 Y", "%Y%m%d%H%M%S"))
    
    print(update(info, _id, tick))

