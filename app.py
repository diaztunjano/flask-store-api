from flask import Flask

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


@app.route("/store", methods=["GET"])
def get():
    return {"stores": stores}
