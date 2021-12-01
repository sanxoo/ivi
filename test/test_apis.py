import requests
import uuid
import json

def test_jobs():
    info, _id = open("info.json").read(), str(uuid.uuid4())
    url = f"http://localhost:8080/jobs"
    print(f"\n{url}")
    resp = requests.get(url)
    for job in resp.json():
        print(job)
    url = f"http://localhost:8080/jobs"
    print(f"\n{url}")
    data = {"_id": _id, "name": "test job", "info": info, "schedule": "* * * * *"}
    resp = requests.post(url, json=data)
    print(resp.json())
    url = f"http://localhost:8080/jobs/{_id}"
    print(f"\n{url}")
    resp = requests.get(url)
    print(resp.json())
    url = f"http://localhost:8080/jobs/{_id}"
    print(f"\n{url}")
    data = {"schedule": "0 0 0 * *"}
    resp = requests.patch(url, json=data)
    print(resp.json())
    url = f"http://localhost:8080/jobs/{_id}"
    print(f"\n{url}")
    resp = requests.delete(url)
    url = f"http://localhost:8080/jobs"
    print(f"\n{url}")
    resp = requests.get(url)
    for job in resp.json():
        print(job)

def test_test():
    url = f"http://localhost:8080/test"
    print(f"\n{url}")
    data = json.load(open("info.json"))["fetch"]
    resp = requests.post(url, json=data)
    for item in resp.json():
        print(item)

if __name__ == "__main__":
    test_jobs()
    test_test()

