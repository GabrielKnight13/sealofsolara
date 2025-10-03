from flask import Flask, request, jsonify, send_from_directory
from player import Player

app = Flask(__name__, static_folder="static")
player = Player()

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")
    
@app.route("/ping")
def ping():
    return "pong"

# --- API Endpoints ---
@app.route("/move", methods=["POST"])
def move():
    direction = request.json.get("direction")
    return jsonify(player.move(direction))

@app.route("/grab", methods=["POST"])
def grab():
    return jsonify(player.grab())

@app.route("/use", methods=["POST"])
def use():
    return jsonify(player.use())

@app.route("/talk", methods=["POST"])
def talk():
    return jsonify(player.talk())

@app.route("/cycle_inventory", methods=["POST"])
def cycle_inventory():
    direction = request.json.get("direction")
    return jsonify(player.cycle_inventory(direction))

@app.route("/inventory", methods=["GET"])
def inventory():
    return jsonify(player.to_dict("Inventory check", "neutral"))

# Optional: reset endpoint for "Return to Title"
@app.route("/reset", methods=["POST"])
def reset():
    global player
    player = Player()  # fresh game state
    return jsonify(player.to_dict("Game reset. Welcome back!", "neutral"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)





