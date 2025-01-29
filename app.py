from flask import Flask, request
from index import get_index
from datetime import datetime

app = Flask(__name__)

index = get_index("index.bin")


@app.route('/new', methods=["POST"])
def new_log():  # put application's code here
    global index
    log_id = index.new_file()
    return {"log_id": log_id}


@app.route("/push", methods=["POST"])
def get_log():
    global index

    log_id = request.args.get("id")
    if log_id is None:
        return {"error": "No log id specified"}, 400

    try:
        log_id = int(log_id)
    except ValueError:
        return {"error": "Invalid log id"}, 400

    log_file = index.get_file(log_id)
    if log_file is None:
        return {"error": "No such log"}, 404

    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()}: {request.get_data().decode("utf-8")}\n")

    return {}, 200


if __name__ == '__main__':
    app.run()
