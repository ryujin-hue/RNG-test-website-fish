from flask import Flask, jsonify, session, request, send_from_directory
from flask_cors import CORS
from player import Player
from trng_engine import TrngEngine

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.secret_key = 'super_secret_key_for_game_world'

# Initialize the TRNG engine once
trng_engine = TrngEngine()

@app.route('/start', methods=['POST'])
def start_game():
    """
    Starts a new game by creating a new player instance.
    """
    player = Player()
    session['player_attributes'] = player.get_status()
    return jsonify({
        "message": "Permainan baru telah dimulakan!",
        "player_status": session['player_attributes']
    })

@app.route('/status', methods=['GET'])
def get_status():
    """
    Gets the current status of the player from the session.
    """
    player_attributes = session.get('player_attributes')
    if not player_attributes:
        return jsonify({"error": "Permainan belum dimulakan. Sila panggil /start dahulu."}), 400

    return jsonify(player_attributes)

@app.route('/actions', methods=['GET'])
def get_actions():
    """
    Returns the list of available player actions.
    """
    return jsonify(trng_engine.get_actions())

@app.route('/perform_action', methods=['POST'])
def perform_action():
    """
    Processes a player's chosen action and then triggers a random event.
    """
    player_attributes = session.get('player_attributes')
    if not player_attributes:
        return jsonify({"error": "Permainan belum dimulakan."}), 400

    data = request.get_json()
    action_id = data.get('action_id')
    if not action_id:
        return jsonify({"error": "Sila berikan 'action_id'."}), 400

    # Create a temporary player object to handle logic
    player = Player()
    player.attributes = player_attributes

    # Check for game over condition before proceeding
    if player.is_game_over():
        return jsonify({
            "message": "Permainan telah tamat!",
            "player_status": player.get_status()
        }), 200

    # 1. Apply effects from player's action
    action = trng_engine.get_action_by_id(action_id)
    if not action:
        return jsonify({"error": f"Tindakan '{action_id}' tidak sah."}), 400

    player.apply_effects(action.get('effects', {}))
    action_description = f"Anda memilih untuk {action['description'].lower()}."

    # 2. Trigger and apply a random event from the God System
    random_event = trng_engine.get_random_event()
    player.apply_effects(random_event.get('effects', {}))

    # Update the session with the new player state
    session['player_attributes'] = player.get_status()

    response = {
        "action_description": action_description,
        "event_description": random_event['description'],
        "player_status": player.get_status()
    }

    # Check for game over condition after the turn
    if player.is_game_over():
        response["message"] = "Permainan telah tamat!"

    return jsonify(response)

@app.route('/')
def serve_index():
    """
    Serves the index.html file.
    """
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
