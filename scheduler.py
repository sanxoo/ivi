import os
import logging.handlers
import logging
import time
import multiprocessing
import json

import config
import jobs
import flow

def is_time_to_run(job, tick):
    sch = [s != "*" and [int(n) for n in s.split(",")] or s for s in job["schedule"].strip().split()]
    ttm = time.localtime(tick)
    for s, n in zip(sch, [ttm.tm_min, ttm.tm_hour, ttm.tm_mday, ttm.tm_mon, (ttm.tm_wday + 1) % 7]):
        if s != "*" and n not in s: return False
    return True

def run(job, tick):
    try:
        info, _id, run = json.loads(job["info"]), job["_id"], time.strftime("%Y%m%d%H%M%S", time.localtime(tick))
        logging.info(f"run {_id} {run}")
        status, message = flow.run(info, _id, tick)
        logging.info(f"end {_id} {run} {status} {message}")
        jobs.update(_id, last_run=run)
        jobs.logs.insert(_id=_id, run=run, end=time.strftime("%Y%m%d%H%M%S"), status=status, message=message)
    except Exception as e:
        logging.error(e)

def loop():
    interval = 60
    tick = time.time() // interval * interval + interval
    while 1:
        if tick < time.time():
            try:
                for job in jobs.select():
                    if is_time_to_run(job, tick): multiprocessing.Process(target=run, args=(job, tick)).start()
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
    loop()
    logging.info("scheduler stop.")

