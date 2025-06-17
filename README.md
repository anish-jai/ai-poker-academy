# Poker Pal

A Python-based interactive poker game built with the CMU Graphics library. The project includes AI-driven player behaviors and visual elements such as cards, a poker table, and probabilities.

## Features

- **Interactive Poker Game**: Play Texas Hold'em with AI opponents
- **AI Players**: Multiple AI personalities (Scared, Neutral, Risky, Random)
- **Probability Display**: Real-time hand probability calculations (Press Space!)
- **Visual Interface**: Beautiful graphics with poker table, cards, and animations
- **Customizable Players**: Add/remove players and customize AI types
- **Speed Controls**: Adjust game speed for better experience

## Prerequisites

- Python 3.x (3.7 or higher recommended)
- CMU Graphics Library

## Installation

1. **Clone or download the project** to your local machine
2. **Navigate to the project directory**:
   ```bash
   cd /path/to/pokerpalTP3
   ```
3. **Create and activate a Python virtual environment**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```
4. **Navigate to the src directory**:
   ```bash
   cd src
   ```
5. **Install Python dependencies**:
   ```bash
   pip install cmu-graphics
   ```

## Running the Game

### Method 1: Run from the src directory (Recommended)
```bash
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

cd src
python main.py
```

## Game Controls

### Shortcut Commands
- **Up Arrow**: Increase game speed
- **Down Arrow**: Decrease game speed  
- **Space**: Toggle probability display for your hand

### Game Commands
- **b**: Bet - Match the current bet amount
- **r**: Raise - Raise the bet (enter amount followed by R)
- **f**: Fold - Exit the current hand

### Navigation
- **Left/Right Arrows**: Navigate through game log
- **ESC**: Exit instructions screen

## Game Setup

1. **Player Selection Screen**: 
   - Choose how many players (1-6)
   - Select AI personality types for each player
   - Customize player names
   - Click "Start Game" to begin

2. **AI Personalities**:
   - **Scared**: Conservative player, folds easily
   - **Neutral**: Balanced decision making
   - **Risky**: Aggressive player, bets frequently
   - **Random**: Unpredictable behavior

## Game Rules

- **Texas Hold'em**: Standard poker rules apply
- **Starting Money**: Each player starts with $1000
- **Buy-in**: $10 minimum bet per round
- **Objective**: Win the pot by having the best hand or making others fold

## File Structure

```
pokerpalTP3/
├── README.md
├── readme.txt
└── src/
    ├── main.py          # Main game logic
    ├── Player.py        # Player and AI logic
    ├── Card.py          # Card class and graphics
    ├── Deck.py          # Deck management
    └── images/          # All game graphics
        ├── introScreen.png  # Game intro screen
        ├── instructions.png # Game instructions
        ├── poker_table.png  # Poker table background
        ├── back_card.jpg    # Card back design
        ├── Spades.png       # Spades suit graphics
        ├── Diamonds.png     # Diamonds suit graphics
        ├── Hearts.png       # Hearts suit graphics
        └── Clubs.png        # Clubs suit graphics
```

## Troubleshooting

### Common Issues

1. **"FileNotFoundError: introScreen.png"**
   - **Solution**: Make sure you're running the game from the `src` directory
   - Run: `cd src && python main.py`
   - The game automatically looks for images in the `src/images/` folder

2. **CMU Graphics not found**
   - **Solution**: Install the library: `pip install cmu-graphics`
   - **Make sure your virtual environment is activated first**

3. **Virtual environment activation issues**
   - **Solution**: Ensure you're in the project root directory when creating the virtual environment
   - Run: `python3 -m venv venv` from the project root
   - Activate with: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

4. **Python version issues**
   - **Solution**: Use Python 3.7 or higher

5. **Missing image files**
   - **Solution**: Ensure all image files are in the `src/images/` folder
   - Required files: introScreen.png, instructions.png, poker_table.png, back_card.jpg, Spades.png, Diamonds.png, Hearts.png, Clubs.png

### Performance Tips

- Use arrow keys to adjust game speed for better experience
- Toggle probability display with spacebar to see your winning chances
- Use the game log navigation to review previous actions

## Credits

- **Author**: Anish Jain
- **Graphics**: CMU Graphics library and custom designs
- **Poker Hands Reference**: [Poker Harder](https://www.pokerharder.com/img/p/3/pokerhands_big.jpg)
- **Other Designs**: Canva

## License

This project is for educational purposes. All graphics and code are original or used with appropriate permissions. 