import sys
import os
import io
from contextlib import redirect_stdout

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
    
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        # init engine
        engine.player = None
        engine.world = None
        engine.running = True
        engine.in_combat = False
        engine.active_combat = None

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
    
    output_buffer.getvalue()  # clear buffer
    
    return jsonify({
        'game_id': game_id,
        'player': {
            'name': engine.player.name,
            'race': engine.player.race,
            'health': engine.player.health,
            'max_health': engine.player.max_health
        },
        'messages': games[game_id]['messages'],
        'in_combat': False
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

    print(f"Processing command: '{command_text}'")

    # combat mode: check if player is in combat
    if engine.in_combat:
        print("Player is in combat, handling combat actions")

        if command_text.lower() == "attack":
            result = engine.process_combat_action("attack")
        elif command_text.lower() == "special":
            result = engine.process_combat_action("special")
        elif command_text.lower() == "flee":
            result = engine.process_combat_action("flee")
        elif command_text.lower() == "use item":
            result = engine.process_combat_action("use item", None)
        elif command_text.lower().startswith("use "):
            param = command_text[4:].strip()

            try:
                item_index = int(param) - 1  # convert to zero-based index
                result = engine.process_combat_action("use item", item_index)
            except ValueError:
                result = engine.process_combat_action("use item", param)
        else:
            # invalid combat command
            result = engine.process_combat_action(command_text.lower())
        
        # process combat result
        combat_log = result.get("log", [])
        
        # format the response
        response = {
            'player': {
                'name': engine.player.name,
                'health': engine.player.health,
                'max_health': engine.player.max_health,
                'inventory': [item.name for item in engine.player.inventory]
            },
            'messages': [f"> {command_text}"] + combat_log,
            'in_combat': engine.in_combat,
            'game_over': engine.player.health <= 0 or not engine.running
        }
        
        # add enemy info if still in combat
        if engine.in_combat and engine.active_combat:
            enemy_state = result.get("enemy", {})
            response['enemy'] = enemy_state
        
        return jsonify(response)

    # combat initiation: handle encounter/attack commands to start combat
    if command_text.lower() == "encounter" or command_text.lower().startswith("attack "):
        print("Starting combat")
        
        if command_text.lower() == "encounter":
            result = engine.start_combat()
        else:
            enemy_name = command_text[7:].strip()  # remove 'attack ' prefix
            result = engine.start_combat(enemy_name)

        if "error" in result:
            return jsonify({
                'player': get_player_data(engine.player),
                'messages': [f"> {command_text}"] + result.get("log", ["Combat failed to start"]),
                'in_combat': False,
                'game_over': False
            })
        
        # combat started successfully
        combat_log = result.get("log", [])
        enemy_data = result.get("enemy", {})
        
        return jsonify({
            'player': get_player_data(engine.player),
            'enemy': enemy_data,
            'messages': [f"> {command_text}"] + combat_log,
            'in_combat': True,
            'game_over': False
        })

    if command_text.lower() == "quit":
        engine.running = False

        return jsonify({
            'player': get_player_data(engine.player),
            'messages': ["> quit", "Goodbye, traveler! Returning to main menu..."],
            'game_over': True,
            'quit': True
        })

    # normal mode: process regular non-combat commands
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        try:
            result = process_command(command_text, engine)

            if result:
                print(result)
        except Exception as e:
            print(f"Error processing command: {e}")
            result = f"Error: {str(e)}"
    
    captured_output = output_buffer.getvalue()

    print(f"Captured output: '{captured_output[:100]}...' (truncated)")

    if captured_output:
        game['messages'] = [f"> {command_text}", captured_output]
    else:
        game['messages'] = [f"> {command_text}", "No response from the game."]

    # return updated game state
    return jsonify({
        'player': get_player_data(engine.player),
        'messages': game['messages'][-10:],  # last 10 messages
        'in_combat': False,
        'game_over': not engine.running or not engine.player.is_alive()
    })

def get_player_data(player):
    return {
        'name': player.name,
        'health': player.health,
        'max_health': player.max_health,
        'inventory': [item.name for item in player.inventory]
    }

if __name__ == '__main__':
    app.run(debug=True)