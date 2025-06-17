# 🃏 AI Poker Academy

🎯 A Python-based interactive poker game built with the CMU Graphics library. The project features **Monte Carlo simulation-based probability calculations** for realistic poker odds and AI-driven player behaviors with beautiful visual elements.

Intended for players new to poker or looking to improve probability calculations and decision-making skills at the table.

## ✨ Features

- 🤖 **Interactive Poker Game**: Play Texas Hold'em with AI opponents
- 🎲 **Monte Carlo Simulation Engine**: Real-time poker probability calculations using advanced Monte Carlo methods (up to 10000 simulations per decision)
- 📊 **Live Probability Display**: See your winning chances calculated through Monte Carlo simulation (Press Space!)
- **AI Players**: Multiple AI personalities (Scared, Neutral, Risky, Random) with Monte Carlo-driven decision making
- **Visual Interface**: Beautiful graphics with poker table, cards, and animations
- **Customizable Players**: Add/remove players and customize AI types
- **Speed Controls**: Adjust game speed for better experience

## 🧮 Monte Carlo Simulation Technology

The game uses  **Monte Carlo Methods** to calculate poker probabilities in real-time:

- **Outcome Simulation**: Runs 3000+ random simulations for each hand evaluation
- **Dynamic Probability Calculation**: Accounts for known cards (your hand + community cards) and simulates all possible remaining scenarios
- **AI Decision Making**: Each AI player uses Monte Carlo-calculated "betability" scores to make realistic betting decisions
- **Real-time Updates**: Probabilities update as community cards are revealed throughout each hand

## 📋 Prerequisites

- 🐍 Python 3.x (3.7 or higher recommended)
- CMU Graphics Library

## 🚀 Installation

1. **Clone or download the project** to your local machine
2. **Navigate to the project directory**:
   
```bash
   cd /path/to/ai-poker-academy
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

## 🎮 Running the Game

### Method 1: Run from the src directory (Recommended)
```bash
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

cd src
python main.py
```

## 🎲 Game Controls

### Shortcut Commands
- ⬆️ **Up Arrow**: Increase game speed
- ⬇️ **Down Arrow**: Decrease game speed
- 🔍 **Space**: Toggle Monte Carlo probability display for your hand

### Game Commands
- **b**: Bet - Match the current bet amount 💰
- **r**: Raise - Raise the bet (enter amount followed by R) 📈
- **f**: Fold - Exit the current hand 🙅‍♂️

### Navigation
- **Left/Right Arrows**: Navigate through game log ↔️
- **ESC**: Exit instructions screen

## ⚙️ Game Setup

1. 👥 **Player Selection Screen**: 
   - Choose how many players (1-6) 
   - Select AI personality types for each player
   - Customize player names
   - Click "Start Game" to begin

2. **AI Personalities** (All powered by Monte Carlo simulation):
   - 😰 **Scared**: Conservative player, requires high Monte Carlo confidence to bet
   - 😐 **Neutral**: Balanced decision making based on simulation probabilities
   - 😤 **Risky**: Aggressive player, bets with lower Monte Carlo thresholds
   - 🎲 **Random**: Unpredictable behavior with occasional Monte Carlo influence

## 📖 Game Rules

- **Texas Hold'em**: Standard poker rules apply
- **Starting Money**: Each player starts with $1000 💵
- **Buy-in**: $10 minimum bet per round
- **Objective**: Win the pot by having the best hand or making others fold 🏆
- **Probability Calculations**: All odds calculated using Monte Carlo simulation methods

## 📁 File Structure

```
ai-poker-academy/
├── README.md
└── src/
    ├── main.py          # Main game logic
    ├── Player.py        # Player, AI logic & Monte Carlo simulation engine
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

## 🔧 Troubleshooting

### ❌ Common Issues

1. **"FileNotFoundError: introScreen.png"** 
   - **Solution**: Make sure you're running the game from the src directory
   - Run: `cd src && python main.py`
   - The game automatically looks for images in the src/images/ folder

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
   - **Solution**: Ensure all image files are in the src/images/ folder
   - Required files: introScreen.png, instructions.png, poker_table.png, back_card.jpg, Spades.png, Diamonds.png, Hearts.png, Clubs.png

6. **Monte Carlo simulation running slowly**
   - **Solution**: The game runs 3000+ simulations per decision for accuracy - this is normal
   - Use speed controls (arrow keys) to adjust game pace if needed

### Performance Tips 💡

- Use arrow keys to adjust game speed for better experience
- Toggle Monte Carlo probability display with spacebar to see your winning chances
- Use the game log navigation to review previous actions
- Monte Carlo calculations are most accurate when more community cards are revealed

## 👏 Credits

- **Author**: Anish Jain
- **Monte Carlo Engine**: Custom implementation for poker probability simulation
- **Graphics**: CMU Graphics library and custom designs
- **Poker Hands Reference**: [Poker Harder](https://www.pokerharder.com/img/p/3/pokerhands_big.jpg)
- **Other Designs**: Canva

## 📄 License

This project is for educational purposes. All graphics and code are original or used with appropriate permissions.
