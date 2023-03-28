from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "TheStore",
        "items": [
            {"name": "Chair", "price": 14.5},
            {"name": "Table", "price": 30},
            {"name": "Ladder", "price": 5},
        ],
    }
]


@app.route("/stores", methods=["GET"])
def get_stores():
    return {"stores": stores}


@app.route("/store", methods=["GET", "POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)

    return new_store, 201
