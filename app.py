from flask import Flask, request, jsonify, send_from_directory, session
from player import Player
import uuid

app = Flask(__name__, static_folder="static")
app.secret_key = "your-secret-key"  # Required for session support

game_state_by_player = {}

@app.before_request
def assign_session_id():
    if 'player_id' not in session:
        session['player_id'] = str(uuid.uuid4())

def get_player():
    player_id = session.get('player_id')
    if player_id not in game_state_by_player:
        game_state_by_player[player_id] = Player()
    return game_state_by_player[player_id]

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# --- Unified Action Endpoint (optional) ---
@app.route("/action", methods=["POST"])
def handle_action():
    player = get_player()
    action = request.json.get("action")
    data = request.json.get("data", {})

    if action == "move":
        return jsonify(player.move(data.get("direction")))
    elif action == "grab":
        return jsonify(player.grab())
    elif action == "use":
        return jsonify(player.use())
    elif action == "talk":
        return jsonify(player.talk())
    elif action == "cycle_inventory":
        return jsonify(player.cycle_inventory(data.get("direction")))
    else:
        return jsonify({"error": "Unknown action"}), 400

# --- Individual Endpoints (if preferred) ---
@app.route("/move", methods=["POST"])
def move():
    player = get_player()
    direction = request.json.get("direction")
    return jsonify(player.move(direction))

@app.route("/grab", methods=["POST"])
def grab():
    player = get_player()
    return jsonify(player.grab())

@app.route("/use", methods=["POST"])
def use():
    player = get_player()
    return jsonify(player.use())

@app.route("/talk", methods=["POST"])
def talk():
    player = get_player()
    return jsonify(player.talk())

@app.route("/cycle_inventory", methods=["POST"])
def cycle_inventory():
    player = get_player()
    direction = request.json.get("direction")
    return jsonify(player.cycle_inventory(direction))

@app.route("/inventory", methods=["GET"])
def inventory():
    player = get_player()
    return jsonify(player.to_dict("Inventory check", "neutral"))

@app.route("/reset", methods=["POST"])
def reset():
    player_id = session.get('player_id')
    game_state_by_player[player_id] = Player()
    return jsonify(game_state_by_player[player_id].to_dict("Game reset. Welcome back!", "neutral"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)









