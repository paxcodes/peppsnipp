from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/start")
def main():
    return jsonify({
        "msg": "Hello World!"
    })


if __name__ == "__main__":
    app.run()
