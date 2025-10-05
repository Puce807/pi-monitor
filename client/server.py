
from flask import Flask, jsonify
from client.utilization import get_cpu

app = Flask(__name__)

@app.route("/")
def get_data():

    data = get_cpu()
    return jsonify(data)

# Only start the server if this file is run directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
