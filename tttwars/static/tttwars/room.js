document.addEventListener('DOMContentLoaded', function() {
    const roomName = JSON.parse(document.getElementById('room-id').textContent);

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/'
        + roomName
    );

    // Determining which kind of message it is
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.message != undefined)
        {
            document.querySelector('#chat-log').value += (data.username + ': ' + data.message + '\n');
        }
        else if (data.join != undefined)
        {
            location.reload()
        }
        else if (data.resign != undefined)
        {
            location.reload()
        }
        else if (data.id != undefined && data.newsquare != undefined)
        {
            const thesquare = document.getElementById(`${data.id}`);
            const p1score = document.getElementById('p1score');
            const p2score = document.getElementById('p2score');
            p1score.innerHTML = 'Match Score: ' + data.p1totalscore + '&emsp; Game Score: ' + data.p1score;
            p2score.innerHTML = 'Match Score: ' + data.p2totalscore + '&emsp; Game Score: ' + data.p2score;
            if (data.newsquare === 1)
            {
                thesquare.innerHTML = 'O';
            }
            else if (data.newsquare === 2)
            {
                thesquare.innerHTML = 'D';
            }
            if (data.reload === true)
            {
                location.reload()
            }
        }
    };

    chatSocket.onclose = function() {
        console.error('Chat socket closed unexpectedly');
    };

    setTimeout(() => {
        fetch('/getroom/' + roomName)
        .then(response => response.json())
        .then(game => {
            const players = game['players']
            const userobject = JSON.parse(document.getElementById('username').textContent);
            const username = userobject['username'];
            const funnydiv = document.getElementById('funnystuff');
            if (players.indexOf(username) != -1)
            {
                if (game['active'] === true)
                {
                    if (players.length === 2)
                    {
                        const resignbutton = document.createElement('input');
                        resignbutton.classList.add('btn', 'btn-danger');
                        resignbutton.value = 'Resign';
                        resignbutton.onclick = function() {
                            fetch('/resign/' + roomName, {
                                method: 'PUT',
                                headers: { 'X-CSRFToken': token }
                            })
                            chatSocket.send(JSON.stringify({
                                'resign': 'True'
                            }))
                        }
                        funnydiv.append(resignbutton);
                    }
                    else
                    {
                        const leavebutton = document.createElement('input');
                        leavebutton.classList.add('btn', 'btn-danger');
                        leavebutton.value = 'Leave Lobby';
                        leavebutton.onclick = function() {
                            fetch('/leave/' + roomName, {
                                method: 'PUT',
                                headers: { 'X-CSRFToken': token }
                            })
                            window.location.pathname = '/';
                        }
                        funnydiv.append(leavebutton)
                    }
                }
            }
        })
    })

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) { // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    }

    document.querySelector('#chat-message-submit').onclick = function() {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        const userobject = JSON.parse(document.getElementById('username').textContent);
        const username = userobject['username'];
        if (message != "") {
        chatSocket.send(JSON.stringify({
            'message': message, 'username': username
        }));
        messageInputDom.value = '';
        }
    }

    const token = document.querySelector('meta[name=csrf-token]').content;

    // Starting the game, only if the game was started it will send a request to everyone to reload their page
    fetch('/startgame/' + roomName)
    .then(response => response.json())
    .then(bool => {
        if (bool['started'] === 'True')
        {
            setTimeout(() => {
                chatSocket.send(JSON.stringify({
                    'join': 'True'
                }))
            }, 1000)
        }
        const board = document.getElementById('board');
        fetch('/getroom/' + roomName)
        .then(response => response.json())
        .then(game => {
            board.dataset.gamenumber = game['gamenumber'];
        })
    })
    make_board(chatSocket)
})

function make_board(chatSocket) {
    // Creating the board and adding data to be able to modify the game board
    const board = document.querySelector('#board');
    const roomid = JSON.parse(document.getElementById('room-id').textContent);
    setTimeout(() => {
        fetch('/getroom/' + roomid)
        .then(response => response.json())
        .then(game => {
            // Creating the username and rating and score to go along with the board
            const gameheader = document.createElement('h3');
            gameheader.innerHTML = 'Game ' + game['gamenumber'];
            gameheader.style = 'color: white;';
            board.append(gameheader);
            const p1name = document.createElement('h5');
            if (game['winner'] === game['p1'] && game['winner'] != 'None')
            {
                if ([1, 3, 5].includes(game['gamenumber']))
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
                if ([1, 3, 5].includes(game['gamenumber']))
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
            p1score.id = 'p1score';
            let p1totalscore = game['matchscore1'] + game['score1'];
            p1score.innerHTML = 'Match Score: ' + p1totalscore + '&emsp; Game Score: ' + game['score1'];
            p1score.style = 'color: white;';
            board.append(p1score)
            // Displaying the correct board
            const gamenumber = game['gamenumber'];
            const whichboard = 'board' + gamenumber;
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
                    // Adding event listener to modify game state when clicked
                    square.onclick = function () {
                        const token = document.querySelector('meta[name=csrf-token]').content;
                        const userobject = JSON.parse(document.getElementById('username').textContent);
                        const username = userobject['username'];
                        fetch('/playmove/' + roomid, {
                            method: 'POST',
                            headers: { 'X-CSRFToken': token },
                            body: JSON.stringify({
                                i: i,
                                j: j,
                                username: username
                            })
                        })
                        setTimeout(() => {
                            fetch('/getroom/' + roomid)
                            .then(response => response.json())
                            .then(newgame => {                      
                                if (board.dataset.gamenumber != newgame['gamenumber'])
                                {
                                    var reload = true
                                }   
                                else
                                {
                                    var reload = false
                                }

                                let p1totalscore = newgame['matchscore1'] + newgame['score1'];
                                p1score.innerHTML = 'Match Score: ' + p1totalscore + '&emsp; Game Score: ' + newgame['score1'];
                                let p2totalscore = newgame['matchscore2'] + newgame['score2'];
                                p2score.innerHTML = 'Match Score: ' + p2totalscore + '&emsp; Game Score: ' + newgame['score2'];

                                chatSocket.send(JSON.stringify({
                                    'newsquare': newgame[whichboard][i][j], 'id': `a${i},${j}`, 'reload': reload,
                                    'p1totalscore': p1totalscore, 'p2totalscore': p2totalscore, 'p1score': newgame['score1'],
                                    'p2score': newgame['score2']
                                }))                                
                                if (newgame[whichboard][i][j] === 1)
                                {
                                    this.innerHTML = 'O';
                                }
                                else if (newgame[whichboard][i][j] === 2)
                                {
                                    this.innerHTML = 'D';
                                }
                                if (board.dataset.gamenumber != newgame['gamenumber'])
                                {
                                    board.dataset.gamenumber = newgame['gamenumber'];
                                    location.reload();
                                }
                                else if (newgame['active'] === false)
                                {
                                    location.reload();
                                }
                            })
                        }, 50)
                    }
                    row.append(square);
                }
                board.append(row);
            }
            const p2name = document.createElement('h5');
            if (game['winner'] === game['p2'] && game['winner'] != 'None')
            {
                if ([1, 3, 5].includes(game['gamenumber']))
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
                if ([1, 3, 5].includes(game['gamenumber']))
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
            p2score.id = 'p2score';
            let p2totalscore = game['matchscore2'] + game['score2'];
            p2score.innerHTML = 'Match Score: ' + p2totalscore + '&emsp; Game Score: ' + game['score2'];
            p2score.style = 'color: white;';
            board.append(p2score);
        })
    })
}