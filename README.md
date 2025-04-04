# Mordor Adventure - Web Edition

A modular Zork-inspired text adventure set in Mordor, where players explore the dark realm through rich narrative, strategic combat, and challenging puzzles. This version features a retro CRT-themed web interface.

## 🔥 Features

- **Immersive World Exploration**: Travel through various regions of Mordor
- **Turn-based Combat**: Strategic battles with various enemy types
- **Character Classes**: Choose from Human, Elf, or Orc, each with unique abilities
- **Inventory System**: Collect, use and manage items
- **Retro CRT Interface**: Nostalgic green-screen terminal aesthetic
- **Web-based Game Engine**: Play directly in your browser

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Flask
- Modern web browser

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

3. Start the server:
   ```bash
   cd web/server
   python server.py
   ```

4. Open the game in your browser:
   - Simply open index.html in your browser
   - Or serve it using a simple HTTP server:
     ```bash
     cd web/client
     python -m http.server
     ```
   - Then navigate to `http://localhost:8000`

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
│   ├── engine.py          # Game engine
│   ├── items.py           # Item definitions
│   └── world.py           # World and region definitions
├── web/
│   ├── client/            # Frontend web interface
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # Client-side logic
│   │   ├── assets/        # Static assets
│   │   │   └── fonts/     # Custom fonts including VT323 for terminal look
│   │   └── index.html     # Main page
│   └── server/            # Backend API server
│       └── server.py      # Flask server
└── README.md              # This file
```

## 🛠️ Technical Details

- **Backend**: Python Flask server provides a REST API for game state
- **Frontend**: HTML, CSS, and JavaScript with a retro CRT terminal style
- **Communication**: JSON-based API for commands and state updates
- **State Management**: Server maintains game state between requests

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎮 Terminal Version

Looking for the terminal-only version? Check out the [terminal branch](https://github.com/steepcloud/Mordor-adventure/tree/terminal) for a classic command-line experience.

---

*Disclaimer: This project is a fan creation and is not affiliated with the works of J.R.R. Tolkien or any official Tolkien estate properties.*

Similar code found with 2 license types
