document.addEventListener('DOMContentLoaded', function() {  
    document.querySelector('#room-name-input').focus();
    document.querySelector('#room-name-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#room-name-submit').click();
        }
    };

    document.querySelector('#room-name-submit').onclick = function() {
        var roomName = document.querySelector('#room-name-input').value;
        window.location.pathname = '/' + roomName;
    };

    document.querySelectorAll('.gamelisting').forEach(function(listing) {
        listing.onclick = function () {
            const id = listing.dataset.id;
            const token = document.querySelector('meta[name=csrf-token]').content;
            const currentuserobject = JSON.parse(document.getElementById('username').textContent);
            const currentusername = currentuserobject['username'];
            // Checking if the game already has 2 players
            fetch('/getroom/' + id)
            .then(response => response.json())
            .then(game => {
                // Adding the user to the player list if there is space
                if (game['players'].length < 2)
                {
                    fetch('/getroom/' + id, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': token},
                        body: JSON.stringify({
                            player: currentusername
                        })
                    })
                }
                window.location.replace('/' + id);
            })
        }
    })
})
