```python
# Backend: Flask Application

# Install dependencies
# pip install Flask Flask-Cors SQLAlchemy

# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_data = db.Column(db.Text)

# Game state
class GameState:
    def __init__(self):
        self.pacman = {'x': 1, 'y': 1, 'lives': 3, 'score': 0}
        self.ghosts = [{'x': 5, 'y': 5, 'state': 'Chase'}]
        self.maze = [[0 for _ in range(10)] for _ in range(10)]  # Placeholder for the maze

    def update(self):
        self.move_ghosts()
        # Additional game logic here (collisions, scoring, etc.)

    def move_ghosts(self):
        for ghost in self.ghosts:
            ghost['x'] += random.choice([-1, 0, 1])
            ghost['y'] += random.choice([-1, 0, 1])

game_state = GameState()

@app.route('/start', methods=['POST'])
def start_game():
    game_state.__init__()  # Reset the game state
    return jsonify(game_state.__dict__)

@app.route('/update', methods=['POST'])
def update_game():
    game_state.update()
    return jsonify(game_state.__dict__)

@app.route('/score', methods=['POST'])
def save_score():
    data = request.json
    new_user = User(score=data['score'], level=data['level'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(id=new_user.id)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```javascript
// Frontend: React Application

// Install dependencies
// npx create-react-app pacman-frontend
// cd pacman-frontend
// npm install axios

// src/App.js
import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
    const [gameData, setGameData] = useState(null);
    const [score, setScore] = useState(0);
    const [level, setLevel] = useState(1);

    useEffect(() => {
        startGame();
    }, []);

    const startGame = async () => {
        const response = await axios.post('http://localhost:5000/start');
        setGameData(response.data);
    };

    const updateGame = async () => {
        const response = await axios.post('http://localhost:5000/update');
        setGameData(response.data);
    };

    const saveScore = async () => {
        await axios.post('http://localhost:5000/score', { score: score, level: level });
    };

    return (
        <div>
            <h1>Pacman Game</h1>
            {gameData && (
                <div>
                    <h2>Score: {gameData.pacman.score}</h2>
                    <p>Lives: {gameData.pacman.lives}</p>
                    <button onClick={updateGame}>Update Game</button>
                    <button onClick={saveScore}>Save Score</button>
                </div>
            )}
        </div>
    );
};

export default App;
```