document.addEventListener('DOMContentLoaded', function() {
    const username = window.location.href.split('/')[4];
    const currentuserobject = JSON.parse(document.getElementById('username').textContent);
    const currentusername = currentuserobject['username'];
    // Non owners should be able to friend/unfriend, owner should be able to see the amount of friends and friend list
    if (username != currentusername)
    {
        friend_button();
        document.querySelector('#friendbutton').addEventListener('click', () => friend());
        document.querySelector('#friendbutton').addEventListener('click', () => friend_button());
    }
    else
    {
        load_requests();
    }
})

function friend_button() {
    const username = window.location.href.split('/')[4];
    const currentuserobject = JSON.parse(document.getElementById('username').textContent);
    const currentusername = currentuserobject['username'];

    // Timeout needed to let stuff load, changing the text of the button to show the action it will perform
    setTimeout( () => {
        fetch('/profiles/' + username)
        .then(response => response.json())
        .then(profile => {
            fetch('/profiles/' + currentusername)
            .then(response => response.json())
            .then(requestprofile => {
                const friend_button = document.querySelector('#friendbutton');
                if (profile['friends'].includes(requestprofile['username']) === false && profile['requested'].includes(requestprofile['username']) === false && requestprofile['requested'].includes(profile['username']) === false)
                {
                    friend_button.value = 'Request Friend';
                }
                else if (profile['friends'].includes(requestprofile['username']) === false && profile['requested'].includes(requestprofile['username']) === true)
                {
                    friend_button.value = 'Unrequest Friend';
                }
                else if (profile['friends'].includes(requestprofile['username']) === false && profile['requested'].includes(requestprofile['username']) === false && requestprofile['requested'].includes(profile['username']) === true)
                {
                    friend_button.value = 'Add Friend';
                }
                else
                {
                    friend_button.value = 'Remove Friend';
                }
            })
        })
    }, 30)
}

function friend() {
    
    // Sending or unsending friend request
    const username = window.location.href.split('/')[4];
    const token = document.querySelector('meta[name=csrf-token]').content;
    fetch('/profiles/' + username, {
        method: 'POST',
        headers: { 'X-CSRFToken': token },
        body: JSON.stringify({
            requested: username
        })
    })
}

function load_requests() {
    const username = window.location.href.split('/')[4];
    const currentuserobject = JSON.parse(document.getElementById('username').textContent);
    const currentusername = currentuserobject['username'];
    const token = document.querySelector('meta[name=csrf-token]').content;

    // Getting the friends
    fetch('/profiles/' + username)
    .then(response => response.json())
    .then(profile => {

        // Getting requests that aren't friends already
        let friends = profile['friends'];
        let requests = profile['requested'];
        let filtered = requests.filter(request => !friends.includes(request))
        const body = document.getElementById('profilebody')

        // Showing amount of pending requests
        const requestamountdiv = document.createElement('div');
        if (filtered.length === 1)
        {
            requestamountdiv.innerHTML = filtered.length + ' Friend Request Pending';
        }
        else
        {
            requestamountdiv.innerHTML = filtered.length + ' Friend Requests Pending';
        }
        body.append(requestamountdiv);

        // Creating the div for the requests
        const div = document.createElement('div');
        div.classList.add('d-flex', 'flex-row');

        filtered.forEach(element => {

            // Creating div for each individual request
            const requestdiv = document.createElement('div');
            requestdiv.classList.add('p-2', 'requestblock');

            // Creating div to show username of requestor
            const usernamediv = document.createElement('div');
            usernamediv.innerHTML = element;
            requestdiv.append(usernamediv);

            // Accept and deny buttons for the request
            const button = document.createElement('input');
            button.classList.add('button2', 'accept');
            button.type = 'submit';
            button.value = 'Accept';
            button.onclick = function () {
                fetch('/profile/' + element, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': token },
                    body: JSON.stringify({
                        action: 'accept',
                        requestor: element
                    })
                })
                requestdiv.remove();
            }
            requestdiv.append(button);
            const denybutton = document.createElement('input');
            denybutton.classList.add('button2', 'deny');
            denybutton.type = 'submit';
            denybutton.value = 'Deny';
            denybutton.onclick = function () {
                fetch('/profile/' + element, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': token },
                    body: JSON.stringify({
                        action: 'deny',
                        requestor: element
                    })
                })
                requestdiv.remove();
            }
            requestdiv.append(denybutton);
            div.append(requestdiv);
        })
        body.append(div);
    })
}