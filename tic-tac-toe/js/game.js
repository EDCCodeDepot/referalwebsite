(function () {
    'use strict';

    const PLAYER_X = 'X';
    const PLAYER_O = 'O';

    const WIN_COMBOS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
        [0, 4, 8], [2, 4, 6]              // diagonals
    ];

    let board = Array(9).fill(null);
    let currentPlayer = PLAYER_X;
    let gameOver = false;
    let scores = { X: 0, O: 0, draws: 0 };

    // DOM elements
    const cells = document.querySelectorAll('.cell');
    const statusEl = document.getElementById('status');
    const scoreXEl = document.getElementById('score-x');
    const scoreOEl = document.getElementById('score-o');
    const scoreDrawsEl = document.getElementById('score-draws');
    const restartBtn = document.getElementById('restart-btn');
    const resetBtn = document.getElementById('reset-btn');

    function init() {
        cells.forEach(function (cell) {
            cell.addEventListener('click', handleCellClick);
        });
        restartBtn.addEventListener('click', restartGame);
        resetBtn.addEventListener('click', resetScores);
        updateStatus();
    }

    function handleCellClick(e) {
        var index = parseInt(e.target.dataset.index, 10);

        if (board[index] !== null || gameOver) {
            return;
        }

        board[index] = currentPlayer;
        var cell = e.target;
        cell.textContent = currentPlayer;
        cell.classList.add('taken', currentPlayer.toLowerCase(), 'pop');

        var winCombo = checkWin(currentPlayer);
        if (winCombo) {
            gameOver = true;
            scores[currentPlayer]++;
            updateScoreboard();
            highlightWin(winCombo);
            statusEl.textContent = 'Player ' + currentPlayer + ' wins!';
            statusEl.className = 'status winner turn-' + currentPlayer.toLowerCase();
            return;
        }

        if (board.every(function (cell) { return cell !== null; })) {
            gameOver = true;
            scores.draws++;
            updateScoreboard();
            statusEl.textContent = "It's a draw!";
            statusEl.className = 'status draw';
            return;
        }

        currentPlayer = currentPlayer === PLAYER_X ? PLAYER_O : PLAYER_X;
        updateStatus();
    }

    function checkWin(player) {
        for (var i = 0; i < WIN_COMBOS.length; i++) {
            var combo = WIN_COMBOS[i];
            if (
                board[combo[0]] === player &&
                board[combo[1]] === player &&
                board[combo[2]] === player
            ) {
                return combo;
            }
        }
        return null;
    }

    function highlightWin(combo) {
        combo.forEach(function (index) {
            cells[index].classList.add('winning');
        });
    }

    function updateStatus() {
        statusEl.textContent = "Player " + currentPlayer + "'s turn";
        statusEl.className = 'status turn-' + currentPlayer.toLowerCase();
    }

    function updateScoreboard() {
        scoreXEl.textContent = scores.X;
        scoreOEl.textContent = scores.O;
        scoreDrawsEl.textContent = scores.draws;
    }

    function restartGame() {
        board = Array(9).fill(null);
        gameOver = false;
        currentPlayer = PLAYER_X;

        cells.forEach(function (cell) {
            cell.textContent = '';
            cell.className = 'cell';
        });

        updateStatus();
    }

    function resetScores() {
        scores = { X: 0, O: 0, draws: 0 };
        updateScoreboard();
        restartGame();
    }

    init();
})();
