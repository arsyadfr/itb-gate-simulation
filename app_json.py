from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

FILE = "parking_data.json"

TARIFF = {
    "motor": {"hourly": 2000, "max": 5000, "overnight": 5000},
    "mobil": {"hourly": 3000, "max": 10000, "overnight": 15000},
}


def load():
    # if the file doesn't exist yet, start with empty data
    if not os.path.exists(FILE):
        return {"sessions": {}, "transactions": []}
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def fail(message):
    return jsonify(success=False, message=message), 400


def calc_fee(vehicle, t_in, t_out):
    tariff = TARIFF[vehicle]
    minutes = (t_out - t_in).total_seconds() / 60

    # first 15 minutes are free
    if minutes <= 15:
        fee = 0
    else:
        # round up to the next full hour (without math.ceil)
        hours = int(minutes // 60)
        if minutes % 60 > 0:
            hours += 1
        fee = min(hours * tariff["hourly"], tariff["max"])

    # every midnight crossed adds an overnight fee
    nights = (t_out.date() - t_in.date()).days
    fee += nights * tariff["overnight"]

    # duration is rounded up to the next full minute
    total_minutes = int(minutes)
    if minutes % 1 > 0:
        total_minutes += 1
    return fee, total_minutes


def add_log(data, card_id, owner, vehicle, action, time, duration=0, fee=0, balance_after=None):
    data["transactions"].append({
        "time": time,
        "card_id": card_id,
        "owner": owner,
        "vehicle": vehicle,
        "action": action,
        "duration_minutes": duration,
        "fee": fee,
        "balance_after": balance_after,
    })


@app.route("/", methods=["GET"])
def simulator():
    return render_template("index.html")


@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    # card_ids currently parked, used by the HTML to sync status on refresh
    return jsonify(success=True, sessions=list(load()["sessions"].keys()))


@app.route("/api/entry", methods=["POST"])
def entry():
    body = request.json
    data = load()

    card_id = body["card_id"]
    vehicle = body.get("vehicle")
    if vehicle not in TARIFF:
        return fail("Vehicle type is invalid (motor/mobil).")
    if card_id in data["sessions"]:
        return fail("Vehicle has entered.")

    owner = body.get("owner", "Unknown")
    data["sessions"][card_id] = {
        "owner": owner,
        "vehicle": vehicle,
        "entry_time": body["time"],
    }
    add_log(data, card_id, owner, vehicle, "ENTRY", body["time"],
            balance_after=body.get("balance"))
    save(data)
    return jsonify(success=True, message="Please enter.")


@app.route("/api/exit", methods=["POST"])
def exit_parking():
    body = request.json
    data = load()

    card_id = body["card_id"]
    session = data["sessions"].get(card_id)
    if session is None:
        return fail("Vehicle has not entered.")

    t_in = datetime.fromisoformat(session["entry_time"])
    t_out = datetime.fromisoformat(body["time"])
    if t_out < t_in:
        return fail("Exit time is earlier than entry time.")

    fee, minutes = calc_fee(session["vehicle"], t_in, t_out)

    balance = int(body["balance"])
    if balance < fee:
        return fail("Balance is insufficient.")

    balance_after = balance - fee
    del data["sessions"][card_id]
    add_log(data, card_id, session["owner"], session["vehicle"], "EXIT",
            body["time"], minutes, fee, balance_after)
    save(data)
    return jsonify(success=True, message="Please exit.", fee=fee, balance_after=balance_after)


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    return jsonify(success=True, transactions=load()["transactions"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)