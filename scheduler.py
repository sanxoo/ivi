import os
import logging.handlers
import logging
import time
import json
from multiprocessing import Process

import config
import jobs
import flow

def is_time_to_run(job, tick):
    sch = [s != "*" and [int(n) for n in s.split(",")] or s for s in job["schedule"].strip().split()]
    now = time.localtime(tick)
    for s, n in zip(sch, [now.tm_min, now.tm_hour, now.tm_mday, now.tm_mon, (now.tm_wday + 1) % 7]):
        if s != "*" and n not in s: return False
    return True

def run(job, tick):
    try:
        _id, info = job["_id"], json.loads(job["info"])
        now = time.strftime("%Y%m%d%H%M%S", time.localtime(tick))
        # 
        # fill information
        # 
        info["load"]["file"] = os.path.join(config.file_path, f"{_id}_{now}.csv")
        # 
        logging.info(f"run {_id} {now}")
        status, message = flow.run(_id, info)
        logging.info(f"end {_id} {now} {status} {message}")
        jobs.update(_id, last_run=now)
        jobs.logs.insert(_id=_id, run=now, end=time.strftime("%Y%m%d%H%M%S"), status=status, message=message)
    except Exception as e:
        logging.error(e)

def main():
    interval = 60
    tick = time.time() // interval * interval + interval
    while 1:
        if tick < time.time():
            try:
                for job in jobs.select():
                    if is_time_to_run(job, tick): Process(target=run, args=(job, tick)).start()
            except Exception as e:
                logging.error(e)
            tick += interval
        time.sleep(1)

if __name__ == "__main__":
    logfile = os.path.join(config.logs_path, "scheduler.log")
    handler = logging.handlers.RotatingFileHandler(logfile, "a", 10 * 1024 * 1024, 9)
    handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s:%(lineno)3d : %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logging.info("scheduler start")
    main()
    logging.info("scheduler stop.")

