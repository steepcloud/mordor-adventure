# Mordor Adventure - Terminal Edition

A modular Zork-inspired text adventure set in Mordor, where players explore the dark realm through rich narrative, strategic combat, and challenging puzzles. This classic terminal-based version offers an authentic text adventure experience.

## 🔥 Features

- **Immersive World Exploration**: Travel through various regions of Mordor
- **Turn-based Combat**: Strategic battles with various enemy types
- **Character Classes**: Choose from Human, Elf, or Orc, each with unique abilities
- **Inventory System**: Collect, use and manage items
- **Classic Text Interface**: Authentic text adventure experience
- **Terminal-based**: Play directly in your command line

## 🚀 Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/steepcloud/Mordor-adventure.git
   cd Mordor-adventure
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the game:
   ```bash
   python main.py
   ```

## 🎮 How to Play

1. **Start a New Game**: Enter your character name and select a race
2. **Explore the World**: Use commands to move between regions and discover enemies
3. **Battle Enemies**: Engage in turn-based combat with various tactics
4. **Collect Items**: Find and use items to help in your adventure

### Basic Commands

| Command | Description |
|---------|-------------|
| `look` | View your current surroundings |
| `regions` | List available regions to travel to |
| `travel [region]` | Travel to a specific region |
| `enemies` | List enemies in the current region |
| `encounter` | Start a random combat encounter |
| `attack [enemy]` | Attack a specific enemy |
| `inventory` | View your items |
| `use [item]` | Use an item from your inventory |
| `help` | View all available commands |
| `quit` | Exit the game |

### Combat Commands

During combat, you have these options:
- `attack`: Basic attack
- `special`: Use your character's special ability
- `use [item]`: Use an item during combat
- `flee`: Attempt to escape combat

## 🏗️ Project Structure

```
Mordor-adventure/
├── game/                  # Core game logic
│   ├── characters.py      # Character classes and attributes
│   ├── combat.py          # Combat system
│   ├── commands.py        # Command processing
│   ├── command_processor.py # Command handling
│   ├── engine.py          # Game engine
│   ├── game_object.py     # Base game object class
│   ├── items.py           # Item definitions
│   └── world.py           # World and region definitions
├── main.py                # Main game entry point
└── README.md              # This file
```

## 🛠️ Technical Details

- **Python-based**: Pure Python implementation with no external dependencies
- **Object-Oriented**: Modular design with clear separation of concerns
- **Text Interface**: Classic command-line interaction
- **Game State**: In-memory state management during gameplay
- **Input Handling**: Robust command parsing and execution

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌐 Web Version

Looking for a browser-based experience? Check out the [web branch](https://github.com/steepcloud/Mordor-adventure/tree/web) for a retro CRT-themed interface.

---

*Disclaimer: This project is a fan creation and is not affiliated with the works of J.R.R. Tolkien or any official Tolkien estate properties.*
