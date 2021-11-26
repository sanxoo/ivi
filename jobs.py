import sqlite3
import os

_db_name = "jobs.db"

def connect():
    return sqlite3.connect(_db_name)

def init():
    if os.path.exists(_db_name): os.remove(_db_name)
    with connect() as conn:
        cursor = conn.cursor()
        query = "create table jobs ( _id text, name text, info text, schedule text, last_run text )"
        cursor.execute(query)
        conn.commit()

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

