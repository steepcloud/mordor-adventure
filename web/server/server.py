import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from game.engine import GameEngine
from game.commands import process_command

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# store active games
games = {}

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new game instance"""
    data = request.json
    game_id = str(len(games) + 1)
    engine = GameEngine()
    
    # initialize player from request data
    name = data.get('name', 'Adventurer')
    race = data.get('race', 'human')
    
    # store game state
    games[game_id] = {
        'engine': engine,
        'messages': ["Welcome to the Lands of Mordor!"],
    }
    
    # init engine
    engine.player = None
    engine.world = None
    engine.running = True

    # create player based on race
    if race == "orc":
        from game.characters import Orc
        engine.player = Orc(name)
    elif race == "elf":
        from game.characters import Elf
        engine.player = Elf(name)
    else:
        from game.characters import Human
        engine.player = Human(name)
    
    from game.world import World
    engine.world = World(engine.player)
    
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
    
    # get game state
    game = games[game_id]
    engine = game['engine']

    result = process_command(command_text, engine)
    game['messages'] = [f"> {command_text}", result]
    
    # return updated game state
    return jsonify({
        'player': {
            'name': engine.player.name,
            'health': engine.player.health,
            'max_health': engine.player.max_health,
            'inventory': [item.name for item in engine.player.inventory]
        },
        'messages': game['messages'][-10:],  # last 10 messages
        'game_over': not engine.running or not engine.player.is_alive()
    })

if __name__ == '__main__':
    app.run(debug=True)