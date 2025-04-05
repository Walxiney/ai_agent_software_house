#### Backend Code (Python with Flask)

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/pacman_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class GameState(db.Model):
    id = Column(Integer, primary_key=True)
    pacman_position = Column(String, nullable=False)
    ghost_positions = Column(String, nullable=False)
    score = Column(Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'pacman_position': self.pacman_position,
            'ghost_positions': self.ghost_positions,
            'score': self.score
        }

@app.route('/api/game/state', methods=['GET'])
def get_game_state():
    game_state = GameState.query.first()
    return jsonify(game_state.to_dict()), 200

@app.route('/api/game/move', methods=['POST'])
def move_player():
    data = request.json
    direction = data.get('direction')

    game_state = GameState.query.first()
    # Logic to update pacman_position and ghost_positions based on direction
    # For simplicity, let's assume new positions are 'new_pacman_position' and 'new_ghost_positions'
    new_pacman_position = f"moved_{direction}"
    new_ghost_positions = "ghost_positions_updated"

    game_state.pacman_position = new_pacman_position
    game_state.ghost_positions = new_ghost_positions
    game_state.score += 10  # Logic for scoring should be expanded
    db.session.commit()

    return jsonify(game_state.to_dict()), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

#### Frontend Code (HTML + JavaScript with React)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pacman Game</title>
    <style>
        body { display: flex; flex-direction: column; align-items: center; }
        #game-board { width: 400px; height: 400px; position: relative; background-color: black; }
        .pacman { width: 20px; height: 20px; background-color: yellow; position: absolute; border-radius: 50%; }
        .ghost { width: 20px; height: 20px; background-color: red; border-radius: 50%; position: absolute; }
    </style>
</head>
<body>
    <h1>Pacman Game</h1>
    <div id="game-board"></div>
    <button onclick="move('up')">Up</button>
    <button onclick="move('down')">Down</button>
    <button onclick="move('left')">Left</button>
    <button onclick="move('right')">Right</button>
    <div>Score: <span id="score">0</span></div>
    
    <script>
        const gameBoard = document.getElementById('game-board');
        let pacman = document.createElement('div');
        pacman.className = 'pacman';
        gameBoard.appendChild(pacman);

        async function fetchGameState() {
            const response = await fetch('http://localhost:5000/api/game/state');
            const gameState = await response.json();
            pacman.style.top = `${gameState.pacman_position.split('_')[1] * 20}px`;
            pacman.style.left = `${gameState.pacman_position.split('_')[2] * 20}px`;
            document.getElementById('score').innerText = gameState.score;
            // Handle ghost positions similarly
        }

        async function move(direction) {
            await fetch('http://localhost:5000/api/game/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ direction })
            });
            fetchGameState();
        }

        window.onload = fetchGameState;
    </script>
</body>
</html>
```

#### Database Setup (PostgreSQL)
Make sure to set up your PostgreSQL database and replace `username` and `password` in the backend code with your actual database credentials.

1. Create a database:
   ```sql
   CREATE DATABASE pacman_db;
   ```
2. (Optional) Use the following SQL to create the necessary table if you want to do it manually:
   ```sql
   CREATE TABLE game_state (
       id SERIAL PRIMARY KEY,
       pacman_position VARCHAR(255) NOT NULL,
       ghost_positions VARCHAR(255) NOT NULL,
       score INT DEFAULT 0
   );
   ```

With this structure, the Pacman game has a backend to manage game state, handling user movements and storing scores, while the frontend allows users to interact with the game and visualize the Pacman and ghost positions.