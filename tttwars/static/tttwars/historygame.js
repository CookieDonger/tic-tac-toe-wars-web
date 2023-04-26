document.addEventListener('DOMContentLoaded', function() {
    const roomName = JSON.parse(document.getElementById('room-id').textContent);
    const token = document.querySelector('meta[name=csrf-token]').content;
    make_board()
})

function make_board() {
    // Creating the board and adding data to be able to modify the game board
    const board = document.querySelector('#board');
    const roomid = JSON.parse(document.getElementById('room-id').textContent);
    fetch('/getroom/' + roomid)
    .then(response => response.json())
    .then(game => {
        for (let i = 1; i < 7; i++)
        {
            // Creating the username and rating and score to go along with the board
            const gameheader = document.createElement('h3');
            gameheader.innerHTML = 'Game ' + i;
            gameheader.style = 'color: white;';
            board.append(gameheader);
            const p1name = document.createElement('h5');
            if (game['winner'] === game['p1'] && game['winner'] != 'None')
            {
                if ([1, 3, 5].includes(i))
                {
                    p1name.innerHTML = 'Offense: ' + game['p1'] + '(Winner)';
                }
                else
                {
                    p1name.innerHTML = 'Defense: ' + game['p1'] + '(Winner)';
                }
            }
            else
            {
                if ([1, 3, 5].includes(i))
                {
                    p1name.innerHTML = 'Offense: ' + game['p1'];
                }
                else
                {
                    p1name.innerHTML = 'Defense: ' + game['p1'];
                }
            }
            p1name.style = 'color: white; display: inline;';
            board.append(p1name);
            const p1rating = document.createElement('h5');
            p1rating.innerHTML = ' (' + game['p1rating'] + ')';
            p1rating.style = 'display: inline;';
            board.append(p1rating)
            const p1score = document.createElement('h5');
            p1score.innerHTML = 'Match Score: ' + game['p1game' + i + 'score'];
            p1score.style = 'color: white;';
            board.append(p1score)
            // Displaying the correct board
            const whichboard = 'board' + i;
            const gameboard = game[whichboard];
            for (let i = 0; i < 6; i++) {
                const row = document.createElement('div');
                row.classList.add('row');
                for (let j = 0; j < 6; j++) {
                    const square = document.createElement('div');
                    square.classList.add('square');
                    square.dataset.row = i;
                    square.dataset.column = j;
                    square.id = `a${i},${j}`;
                    // Placing either empty square, O (for offense), or D (for defense) in each square
                    if (gameboard[i][j] === 1)
                    {
                        square.innerHTML = 'O';
                    }
                    else if (gameboard[i][j] === 2)
                    {
                        square.innerHTML = 'D';
                    }
                    row.append(square);
                }
                board.append(row);
            }
            const p2name = document.createElement('h5');
            if (game['winner'] === game['p2'] && game['winner'] != 'None')
            {
                if ([1, 3, 5].includes(i))
                {
                    p2name.innerHTML = 'Defense: ' + game['p2'] + '(Winner)';
                }
                else
                {
                    p2name.innerHTML = 'Offense: ' + game['p2'] + '(Winner)';
                }
            }
            else
            {
                if ([1, 3, 5].includes(i))
                {
                    p2name.innerHTML = 'Defense: ' + game['p2'];
                }
                else
                {
                    p2name.innerHTML = 'Offense: ' + game['p2'];
                }
            }
            p2name.style = 'color: white; display: inline;';
            board.append(p2name);
            const p2rating = document.createElement('h5');
            p2rating.innerHTML = ' (' + game['p2rating'] + ')';
            p2rating.style = 'display: inline;';
            board.append(p2rating);
            const p2score = document.createElement('h5');
            p2score.innerHTML = 'Match Score: ' + game['p2game' + i + 'score'];
            p2score.style = 'color: white;';
            board.append(p2score);
            let linebreak = document.createElement('br');
            board.append(linebreak);
        }
    })
}