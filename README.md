# Tic Tac Toe Wars on the Web!
#### Description: A site that allows you to play full matches of tic tac toe wars with others on the website.

<br>
<br>

### Distinctiveness and Complexity:

<p>
While the website does take features of friends from the other projects, it alters it slightly by introducing a friend
request system where both parties must send a friend request to each other to become friends.
</p>

<p> 
The main part of the website though is the ability to play with others on the web and communicate with each other as well. The site uses a lobby system
to create games between players and within each room users are able to play moves and also chat with each other. There is also
a rating system where your rating will go down or up with every loss or win that you get (No movement for draws). The rooms are
also set up so that it can handle both real-time moves through the use of Javascript and Django Channels or a long game through 
multiple games even if you leave the site through the use of Django models which players modify throughout the match.
</p>

<p>
Aside from that, you can find a history of your matches through the history tab and on your profile, find all list of all your
friends and on the play tab, find a list of all the open games and all of the games that you're currently playing. Because of this,
you're required to make an account and login to actually start playing so that it's possible to record the games down.
</p>

<p>
Thus, while this project does take some elements from the other projects, such as friends and the history tab, the overall service
of the website is much different and instead is focused on porting my Tic Tac Toe Wars game (from cs50p) to the web, and most importantly
supports direct communication between users.
</p>

### Running the Server
<p>
To run the server, download the source code and then create a venv and download all of the files in the requirements.txt into it. Then, you need to start a redis port on port 6379, you can find a simple way to do so here: https://stackoverflow.com/questions/41371402/connecting-to-redis-running-in-docker-container-from-host-machine. Once you have done that, you can simply run python3 manage.py runserver in the main directory to run the server and it should start up a webpage at 127.0.0.1:8000.
</p>

## Files

### tttwars/ Directory

#### admin.py

<p>
This just creates the admin website so that I was able to modify the models for testing purposes.
</p>

#### consumers.py

<p>
This contains the ChatConsumer for every room. The overall method of communication between users is the user's JavaScript sending messages
to the WebSocket, which in turn sends messages to the ChatConsumer. The ChatConsumer decides what to do with the message and then sends back
information to the WebSocket, which will then send it to every person's JavaScript to update the page. This handles both the chat messaging
and the playing of moves.
</p>

#### routing.py

<p>
This is like an urls.py but for the WebSocket, because WebSocket requests apparently should be using different urls to distinguish them from
the normal urls.
</p>

#### models.py

Contains 3 different models:
* The User model which only holds 2 extra fields for friends and rating aside from the default fields.
* The Friend Request model which is used to simulate friend requests and requiring for both parties to send a friend request to become friends
* The TTTWarsGame model, which holds the players in the game and their ratings when they started the match, who's chosen as player1 and player2, information to simulate the game while it's being played such as movecount and the current scores, information for each game within the match for recording purposes and the winner if there is one.

#### urls.py

<p>
Holds all of the paths in views.py, including the API routes
</p>

#### views.py

<p>
This holds the various routes for the different pages, holds the API routes for retrieving the User Objects and the TTTWars Objects, holds the login, the register, and the logout page routes. It also holds the routes for creating TTTWarsGames and making the lobbies, along with starting them and the game logic for checking score, checking for legality of moves, checking whether to end the game as well. However, the checking functions were very long so I decided to put them mostly into a helpers.py file in order to have this file focus less on the actual game logic
</p>

#### helpers.py

<p>
A lot of this is taken from my cs50p final project, where I've brought in the check move functions, along with all of the check score functions for all of the various methods for a player to score. This also holds the end_game function, which is used to determine whether to end a game (and along with that, if needed, the entire match itself) and record the data to the TTTWarsGame object and save it.
</p>

### templates/tttwars/ and the static/tttwars/ Directory

#### layout.html

<p>
This holds the layout page which every other html page takes from, it provides the top hand bar for accessing different pages along with logic for changing what's on there depending on if the user is logged in or not. Provides blocks for the title, script, and body. The head also holds the csrf_token for the page so that the JS can access it along with the username of the user that is currently logged in.
</p>

#### index.html

<p>
I actually put all of the important things into the other pages, so the index page just has some text telling the user to play a game.
</p>

#### play.html and play.js

<p>
If the user is logged in, it will bring up a page where there is a button that allows you to create a lobby through JS and redirect you to the page for that lobby. Along with this, it will have a search bar to enter a room number to allow you to spectate a game that has already started (It will not join you into the game as a player if it is not full). Below, there's a list of open games which you can join and the games that have already started that you are playing in, where clicking on any of the entries will redirect you to that game's room page.
</p>

#### room.html and room.js

<p>
The room.html file only holds the basic layout and the room-id so that the JS can access it. The JS will call a make_board function which will create the game board by getting information from the API about the gamestate. This includes the players, their ratings, their match scores and their game scores, along with the moves that have been played on the board. Each square is also given an EventListener for a click that will send a POST request to the API to attempt to modify the gamestate (The logic for checking if the move can be played is in the views.py file).
</p>

<p>
This also creates the WebSocket for communicating between users, whenever the chat button is sent or a square is clicked, JS will send information to the WebSocket to send to other users. The JS will also receive information from the WebSocket, and determine what to do with it depending on if it's a move or if it's a chat message, and what the move did to the gamestate.
</p>

#### profile.html and profile.js

<p>
This page will hold the username of the profile, the date that the user joined, their rating, and how many pending friend requests that they currently have (If they are the owner). Below that is their friends list where clicking on any of the entries will bring you to that person's page. If you are not the owner of the profile you will also be given a button to either friend, unfriend, or send a friend request depending on your current relationship with that user.
</p>

#### friends.html

<p>
This shows your friends list and your friend count just like the profile page, where clicking on any of the profiles will bring you to that page. However, it also has a search input where you can search to find new friends. If the username (Case Sensitive) exists, then it will bring you to that page. If not, it will just give you an error message saying so.
</p>

#### history.html and history.js

<p>
It works the same way as the play page, except that there's only a list for your finished games. It's on it's own page because it will redirect you to the historygame page rather than the game page (Which is slightly different)
</p>

#### historygame.html and historygame.js

<p>
Is similar to the room page, but it does not have a chat box nor will clicking on any of the squares do anything. Rather, the JS is used to load up every game from the match (Which is why I decided to save them all in the Django Model) so that you can see how the match progressed through each game.
</p>

#### login.html and register.html

<p>
You can't access the register page directly from the top bar, instead it's a link on the login page (The register page also has a link back). I did it this way because I saw a lot of pages doing this as well, so I thought it would be nicer to do it this way. The register page will create a new User object and the login page will log you in.
</p>

#### styles.css

<p>
I actually decided to put alot more of the css styling within the HTML and JS because I found putting literally all of the CSS in one file started to get a bit too confusing. Anyways, the CSS gives the body the dark background color (Inspired by Chess.com) and the grey font color as well. Aside from that, it holds the css for forms, the navbar, links, game listings, and the squares for the board.
</p>