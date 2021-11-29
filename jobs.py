import sqlite3

_db_name = "jobs.db"

def connect():
    return sqlite3.connect(_db_name)

def insert(**kwargs):
    with connect() as conn:
        cursor = conn.cursor()
        keys = ["_id", "name", "info", "schedule"]
        vals = "', '".join([kwargs[k] for k in keys])
        query = f"insert into jobs ( {', '.join(keys)}, last_run ) values ( '{vals}', '' ) "
        cursor.execute(query)
        conn.commit()

def select(_id=None):
    with connect() as conn:
        cursor = conn.cursor()
        keys = ["_id", "name", "info", "schedule", "last_run"]
        where = _id and f"where _id = '{_id}' " or ""
        query = f"select {', '.join(keys)} from jobs {where} "
        cursor.execute(query)
        return [dict(zip(keys, row)) for row in cursor]

def update(_id, **kwargs):
    with connect() as conn:
        cursor = conn.cursor()
        equel = ", ".join([f"{k} = '{v}'" for k, v in kwargs.items()])
        query = (
            f"update jobs set {equel} where _id = '{_id}' "
        )
        cursor.execute(query)
        conn.commit()

def delete(_id):
    with connect() as conn:
        cursor = conn.cursor()
        query = f"delete from jobs where _id = '{_id}' "
        cursor.execute(query)
        conn.commit()

class logs:
    def insert(**kwargs):
        with connect() as conn:
            cursor = conn.cursor()
            keys = ["_id", "run", "end", "status", "message"]
            vals = "', '".join([kwargs[k] for k in keys])
            query = f"insert into logs ( {', '.join(keys)} ) values ( '{_id}', '{vals}' ) "
            cursor.execute(query)
            conn.commit()

    def select(**kwargs):
        with connect() as conn:
            cursor = conn.cursor()
            keys = ["_id", "run", "end", "status", "message"]
            where = ""
            for k in keys:
                if k not in kwargs: continue
                value = kwargs[k]
                where = where and where + f"and {k} = '{value}' " or f"where {k} = '{value}' "
            if "from" in kwargs:
                value = kwargs["from"]
                where = where and where + f"and '{value}' <= run " or f"where '{value}' <= run "
            if "to" in kwargs:
                value = kwargs["to"]
                where = where and where + f"and run < '{value}' " or f"where run < '{value}' "
            query = f"select {', '.join(keys)} from logs {where} order by run "
            cursor.execute(query)
            return [dict(zip(keys, row)) for row in cursor]

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", action="store_true", help="init database")
    group.add_argument("-l", "--logs", action="store_true", help="show logs")
    args = parser.parse_args()
    if args.init:
        if os.path.exists(_db_name): os.remove(_db_name)
        with connect() as conn:
            cursor = conn.cursor()
            query = "create table jobs ( _id text, name text, info text, schedule text, last_run text )"
            cursor.execute(query)
            query = "create table logs ( _id text, run text, end text, status text, message text )"
            cursor.execute(query)
            conn.commit()
    elif args.logs:
        for log in logs.select():
            print(f"{log['_id']} {log['run']} {log['end']} {log['status']} {log['message']}")
    else:
        for job in select():
            print(f"{job['_id']} {job['name']} {job['schedule']} {job['last_run']}")
            print(f"{job['info']}")

