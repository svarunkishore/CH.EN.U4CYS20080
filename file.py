from flask import Flask, request, jsonify
import requests
import gevent
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data:
                return set(data["numbers"])
    except:
        pass
    return set()

@app.route("/numbers", methods=["GET"])
def get_merged_numbers():
    urls = request.args.getlist("url")
    jobs = [gevent.spawn(fetch_numbers, url) for url in urls]
    gevent.joinall(jobs, timeout=5)

    merged_numbers = set()
    for job in jobs:
        numbers = job.value
        if numbers:
            merged_numbers.update(numbers)

    merged_numbers = sorted(merged_numbers)
    return jsonify({"numbers": merged_numbers})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
