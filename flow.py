from prefect import Flow

import task

def run(_id, info):
    with Flow(_id) as flow:
        items = task.fetch(info["fetch"])
        task.store(info["store"], items)
    result = flow.run()
    status = result.is_successful() and "succ" or "fail"
    return status, result.message

