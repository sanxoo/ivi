import sys; sys.path.append("..")

import json
from datetime import datetime

import sida

def test_update():
    info, _id, tick = json.load(open("info.json")), "_id", datetime.today().timestamp()
    print(sida.update(info, _id, tick))

if __name__ == "__main__":
    test_update()

