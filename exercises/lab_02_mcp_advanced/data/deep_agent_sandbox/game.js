const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const box = 20; // size of the snake square
const canvasSize = 400;
let snake = [{ x: 9 * box, y: 10 * box }];
let direction = null;
let food = randomFood();
let score = 0;
let gameInterval;

function randomFood() {
    return {
        x: Math.floor(Math.random() * (canvasSize / box)) * box,
        y: Math.floor(Math.random() * (canvasSize / box)) * box
    };
}

function draw() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw snake
    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = i === 0 ? '#0f0' : '#fff';
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
    }

    // Draw food
    ctx.fillStyle = '#f00';
    ctx.fillRect(food.x, food.y, box, box);

    // Move snake
    let head = { x: snake[0].x, y: snake[0].y };
    if (direction === 'LEFT') head.x -= box;
    if (direction === 'UP') head.y -= box;
    if (direction === 'RIGHT') head.x += box;
    if (direction === 'DOWN') head.y += box;

    // Check collision with wall
    if (
        head.x < 0 || head.x >= canvas.width ||
        head.y < 0 || head.y >= canvas.height ||
        collision(head, snake)
    ) {
        clearInterval(gameInterval);
        alert('Game Over! Your score: ' + score);
        document.location.reload();
        return;
    }

    // Check if snake eats food
    if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById('score').innerText = 'Score: ' + score;
        food = randomFood();
    } else {
        snake.pop();
    }

    snake.unshift(head);
}

function collision(head, array) {
    for (let i = 0; i < array.length; i++) {
        if (head.x === array[i].x && head.y === array[i].y) {
            return true;
        }
    }
    return false;
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' && direction !== 'RIGHT') direction = 'LEFT';
    else if (e.key === 'ArrowUp' && direction !== 'DOWN') direction = 'UP';
    else if (e.key === 'ArrowRight' && direction !== 'LEFT') direction = 'RIGHT';
    else if (e.key === 'ArrowDown' && direction !== 'UP') direction = 'DOWN';
});

function startGame() {
    direction = 'RIGHT';
    gameInterval = setInterval(draw, 100);
}

startGame();
