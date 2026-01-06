const boardSize = 20;
const board = document.getElementById('game-board');
const scoreDisplay = document.getElementById('score');
let snake = [{ x: 10, y: 10 }];
let direction = { x: 0, y: 0 };
let food = { x: 5, y: 5 };
let score = 0;
let gameInterval;

function createBoard() {
    board.innerHTML = '';
    for (let y = 0; y < boardSize; y++) {
        for (let x = 0; x < boardSize; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.id = `cell-${x}-${y}`;
            board.appendChild(cell);
        }
    }
}

function draw() {
    // Clear board
    document.querySelectorAll('.cell').forEach(cell => {
        cell.classList.remove('snake', 'food');
    });
    // Draw snake
    snake.forEach(segment => {
        const cell = document.getElementById(`cell-${segment.x}-${segment.y}`);
        if (cell) cell.classList.add('snake');
    });
    // Draw food
    const foodCell = document.getElementById(`cell-${food.x}-${food.y}`);
    if (foodCell) foodCell.classList.add('food');
}

function moveSnake() {
    const newHead = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };
    // Check collision with wall
    if (
        newHead.x < 0 || newHead.x >= boardSize ||
        newHead.y < 0 || newHead.y >= boardSize
    ) {
        gameOver();
        return;
    }
    // Check collision with self
    if (snake.some(segment => segment.x === newHead.x && segment.y === newHead.y)) {
        gameOver();
        return;
    }
    snake.unshift(newHead);
    // Check if food eaten
    if (newHead.x === food.x && newHead.y === food.y) {
        score++;
        scoreDisplay.textContent = `Score: ${score}`;
        placeFood();
    } else {
        snake.pop();
    }
}

function placeFood() {
    let newFood;
    while (true) {
        newFood = {
            x: Math.floor(Math.random() * boardSize),
            y: Math.floor(Math.random() * boardSize)
        };
        if (!snake.some(segment => segment.x === newFood.x && segment.y === newFood.y)) {
            break;
        }
    }
    food = newFood;
}

function gameOver() {
    clearInterval(gameInterval);
    alert('Game Over! Your score: ' + score);
    // Reset game
    snake = [{ x: 10, y: 10 }];
    direction = { x: 0, y: 0 };
    score = 0;
    scoreDisplay.textContent = 'Score: 0';
    placeFood();
    draw();
}

function gameLoop() {
    if (direction.x !== 0 || direction.y !== 0) {
        moveSnake();
    }
    draw();
}

function changeDirection(e) {
    switch (e.key) {
        case 'ArrowUp':
            if (direction.y !== 1) direction = { x: 0, y: -1 };
            break;
        case 'ArrowDown':
            if (direction.y !== -1) direction = { x: 0, y: 1 };
            break;
        case 'ArrowLeft':
            if (direction.x !== 1) direction = { x: -1, y: 0 };
            break;
        case 'ArrowRight':
            if (direction.x !== -1) direction = { x: 1, y: 0 };
            break;
    }
}

document.addEventListener('keydown', changeDirection);

createBoard();
draw();
placeFood();
gameInterval = setInterval(gameLoop, 120);
