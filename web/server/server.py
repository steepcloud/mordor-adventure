from flask import Flask, request, jsonify
from flask_cors import CORS
from game.engine import GameEngine

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Store active games
games = {}

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new game instance"""
    data = request.json
    game_id = str(len(games) + 1)
    engine = GameEngine()
    
    # Initialize player from request data
    name = data.get('name', 'Adventurer')
    race = data.get('race', 'human')
    
    # Store game state
    games[game_id] = {
        'engine': engine,
        'messages': ["Welcome to the Lands of Mordor!"],
    }
    
    # Start game with provided character info
    engine.player = engine._create_player(name, race)
    engine._give_starting_items()
    
    return jsonify({
        'game_id': game_id,
        'player': {
            'name': engine.player.name,
            'race': engine.player.race,
            'health': engine.player.health,
            'max_health': engine.player.max_health
        },
        'messages': games[game_id]['messages']
    })

@app.route('/api/command', methods=['POST'])
def command():
    """Process a command in an active game"""
    data = request.json
    game_id = data.get('game_id')
    command_text = data.get('command')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    # Get game state
    game = games[game_id]
    engine = game['engine']
    
    # Process command
    result = engine.process_command(command_text)
    game['messages'].append(f"> {command_text}")
    game['messages'].append(result)
    
    # Return updated game state
    return jsonify({
        'player': {
            'name': engine.player.name,
            'health': engine.player.health,
            'max_health': engine.player.max_health,
            'inventory': [item.name for item in engine.player.inventory]
        },
        'messages': game['messages'][-10:],  # Last 10 messages
        'game_over': not engine.running or not engine.player.is_alive()
    })

if __name__ == '__main__':
    app.run(debug=True)