from flask import Flask, jsonify, session
from flask_cors import CORS
from player import Player
from trng_engine import TrngEngine

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
# Secret key is needed to use sessions
app.secret_key = 'super_secret_key_for_game_world'

# Initialize the TRNG engine once
trng_engine = TrngEngine()

@app.route('/start', methods=['POST'])
def start_game():
    """
    Starts a new game by creating a new player instance.
    The player's state is stored in the session.
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

@app.route('/next_turn', methods=['POST'])
def next_turn():
    """
    Processes the next turn: gets a random event and applies it to the player.
    """
    player_attributes = session.get('player_attributes')
    if not player_attributes:
        return jsonify({"error": "Permainan belum dimulakan. Sila panggil /start dahulu."}), 400

    # Create a temporary player object to handle logic
    player = Player()
    player.attributes = player_attributes

    # Check for game over condition before proceeding
    if player.is_game_over():
        return jsonify({
            "message": "Permainan telah tamat!",
            "player_status": player.get_status()
        }), 200

    # Get a random event from the TRNG engine
    event = trng_engine.get_random_event()

    # Apply the event's effects
    player.apply_effects(event.get('effects', {}))

    # Update the session with the new player state
    session['player_attributes'] = player.get_status()

    response = {
        "event_description": event['description'],
        "player_status": player.get_status()
    }

    # Check for game over condition after the event
    if player.is_game_over():
        response["message"] = "Permainan telah tamat!"

    return jsonify(response)

if __name__ == '__main__':
    # Using port 5001 to avoid potential conflicts
    app.run(debug=True, port=5001)
