import json
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.db import IntegrityError
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
import re
import random

from .models import User, FriendRequest, TTTWarsGame
from .helpers import check_legal, check_possible, check_score, end_game


def index(request):
    return render(request, "tttwars/index.html")


# Showing all active games
@login_required
def play(request):
    # Damn this annotate and filter stuff really is wild, guess I don't know much about SQL after all
    activegames = TTTWarsGame.objects.filter(active=True).annotate(num_players=Count('players')).filter(num_players__lt=2).exclude(players=request.user)
    mygames = TTTWarsGame.objects.filter(active=True, players=request.user)
    return render(request, "tttwars/play.html", {"active_games": activegames, "my_games": mygames})


# Using the global variable to keep track of count of games so there aren't overlaps of urls
@login_required
def create_room(request):
    if request.method == "POST":
        game = TTTWarsGame()
        game.save()
        game.players.add(request.user)
        return HttpResponseRedirect(reverse('room', kwargs={'room_id': game.id}))


def get_room(request, game_id):
    if request.method == "POST":
        data = json.loads(request.body)
        game = TTTWarsGame.objects.get(id=game_id)
        if game.active is True:
            # Only add the player if there is space (Backend check because frontend is not trustworthy)
            if game.players.count() < 2:
                player = User.objects.get(username=data['player'])
                game.players.add(player)
            else:
                return JsonResponse({'error': 'Game is already full.'}, status=404)
        return HttpResponse(status=204)
    if request.method == "GET":
        if game := TTTWarsGame.objects.get(id=game_id):
            return JsonResponse(game.serialize())
        else:
            return JsonResponse({'error': 'Game does not exist.'}, status=404)


@login_required
def room(request, room_id):
    return render(request, "tttwars/room.html", {"room_id": room_id})


@login_required
def start_game(request, game_id):
    if request.method == "GET":
        game = TTTWarsGame.objects.get(id=game_id)
        if game.active is True:
            # Only start the game if there are 2 players
            if game.players.count() == 2 and not game.p1 and not game.p2:
                players = game.players.all()
                # Randomly choosing who is offense and defense
                p1 = random.choice(players)
                players = players.exclude(username=p1)
                p2 = players[0]
                game.p1 = User.objects.get(username=p1)
                game.p2 = User.objects.get(username=p2)
                game.p1rating = game.p1.rating
                game.p2rating = game.p2.rating
                game.started = True
                game.save()
                return JsonResponse({'started': 'True'})
        return JsonResponse({'started': 'False'})


# Leaves the game if it hasn't started, and if no one is in the lobby then deletes it
@login_required
def leave_game(request, room_id):
    if request.method == "PUT":
        game = TTTWarsGame.objects.get(id=room_id)
        if game.active is True:
            game.players.remove(request.user)
            if game.players.count() == 0:
                game.delete()
        return HttpResponseRedirect(reverse('index'))


# Resigns the game if it has started and ends the game
@login_required
def resign(request, room_id):
    if request.method == "PUT":
        game = TTTWarsGame.objects.get(id=room_id, active=True)
        winner = game.players.exclude(username=request.user.username)
        winner = winner[0]
        game.winner = winner
        game.active = False
        newrating = request.user.rating - 8
        request.user.rating = newrating
        request.user.save()
        newrating = winner.rating + 8
        winner.rating = newrating
        winner.save()
        game.save()
        return HttpResponseRedirect(reverse('index'))


@login_required
def play_move(request, game_id):
    if request.method == "POST":
        if game := TTTWarsGame.objects.get(id=game_id):
            if game.active is True:
                data = json.loads(request.body)
                user = User.objects.get(username=data['username'])
                i = data['i']
                j = data['j']
                boardnum = game.gamenumber
                # Determining which board to use (6 game match because Offense and Defense aren't even)
                if boardnum == 1:
                    gameboard = game.board1
                elif boardnum == 2:
                    gameboard = game.board2
                elif boardnum == 3:
                    gameboard = game.board3
                elif boardnum == 4:
                    gameboard = game.board4
                elif boardnum == 5:
                    gameboard = game.board5
                else:
                    gameboard = game.board6
                movecount = game.movecount
                # Checking if the user is allowed to make a move
                if game.players.filter(username=user.username).exists():
                    # For games 1, 3, 5 (Where p1 will be offense)
                    if game.gamenumber in [1, 3, 5]:
                        if game.p1 == user:
                            # Special case for 1st move
                            if game.movecount == 0:
                                gameboard[i][j] = 1
                                movecount += 1
                            # Rest of moves for offense has to undergo checks
                            elif game.movecount in list(range(1, 36, 2)):
                                if gameboard[i][j] == 0:
                                    if check_legal(gameboard, i, j):
                                        gameboard[i][j] = 1
                                        movecount += 1
                        else:
                            # Defense moves same throughout
                            if game.movecount in list(range(2, 36, 2)):
                                if gameboard[i][j] == 0:
                                    gameboard[i][j] = 2
                                    movecount += 1
                    # For games 2, 4, 6 (Where p2 will be offense)
                    else:
                        if game.p2 == user:
                            # Special case for 1st move
                            if game.movecount == 0:
                                gameboard[i][j] = 1
                                movecount += 1
                            # Rest of moves for offense has to undergo checks
                            elif game.movecount in list(range(1, 36, 2)):
                                if gameboard[i][j] == 0:
                                    if check_legal(gameboard, i, j):
                                        gameboard[i][j] = 1
                                        movecount += 1
                        else:
                            # Defense moves same throughout
                            if game.movecount in list(range(2, 36, 2)):
                                if gameboard[i][j] == 0:
                                    gameboard[i][j] = 2
                                    movecount += 1
                    game.movecount = movecount
                    # Checking if there's possible moves for offense, or if moves are maxed
                    if game.movecount != 0:
                        if not check_possible(gameboard) or movecount == 36:
                            end_game(game=game, gameboard=gameboard)
                        else:
                            # For games 1, 3, 5
                            if game.gamenumber in [1, 3, 5]:
                                game.score1 = check_score(gameboard, "offense")
                                game.score2 = check_score(gameboard, "defense")
                            # For games 2, 4, 6
                            else:
                                game.score1 = check_score(gameboard, "defense")
                                game.score2 = check_score(gameboard, "offense")
                    game.save()
        return HttpResponse(status=204)


@login_required
def profile(request, username):
    if request.method == "POST":
        # For accepting/denying friend requests from the requests section
        data = json.loads(request.body)
        user = request.user
        requestorname = data['requestor']
        requestor = User.objects.get(username=requestorname)
        if data['action'] == 'accept':
            newrequest = FriendRequest(requested=requestor, requestor=user)
            newrequest.save()
            user.friends.add(requestor)
        else:
            previousrequest = FriendRequest.objects.filter(requested=user, requestor=requestor)
            previousrequest.delete()
        return HttpResponse(status=204)
    elif request.method == "GET":
        # Query for profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist.'}, status=404)
        is_owner = False
        if user == request.user:
            is_owner = True
        return render(request, "tttwars/profile.html", {
            "user": user, "is_owner": is_owner
        })


# API using the user's id
@login_required
def get_profile(request, user_id):
    # Query for profile
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist.'}, status=404)

    # Return user information
    if request.method == "GET":
        return JsonResponse(user.serialize())


# API using the user's username
@login_required
def get_profile2(request, username):
    # Query for profile
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist.'}, status=404)

    # Return user information
    if request.method == "GET":
        return JsonResponse(user.serialize())

    elif request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        requested = User.objects.get(username=data['requested'])
        # Checking if the user already has a friend request sent
        if FriendRequest.objects.filter(requested=requested, requestor=user).exists():
            FriendRequest.objects.filter(requested=requested, requestor=user).delete()
        else:
            newrequest = FriendRequest(requested=requested, requestor=user)
            newrequest.save()

        # Checking if the receiver has sent a friend request too and then adding as friends if they both have
        if FriendRequest.objects.filter(requested=requested, requestor=user).exists() and FriendRequest.objects.filter(requested=user, requestor=requested).exists():
            user.friends.add(requested)
        else:
            user.friends.remove(requested)
        return HttpResponse(status=204)


@login_required
def friends(request):
    friends = request.user.friends.all()
    if request.method == "POST":
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
        else:
            return render(request, 'tttwars/friends.html', {
                'friends': friends, 'error': 'User does not exist'
            })
    if request.method == "GET":
        return render(request, "tttwars/friends.html", {
            "friends": friends
        })


@login_required
def history(request):
    if request.method == "GET":
        games = TTTWarsGame.objects.filter(players=request.user, active=False)
        return render(request, 'tttwars/history.html', {
            'games': games
        })


def history_game(request, game_id):
    if request.method == "GET":
        return render(request, 'tttwars/historygame.html', {"room_id": game_id})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Backend checking to make sure fields are correct
        if username == "" or password == "" or confirmation == "":
            return render(request, "tttwars/register.html", {
                "message": "All fields must be filled out"
            })
        # Making sure password is strong enough
        if len(password) < 8:
            return render(request, "tttwars/register.html", {
                "message": "Password must be at least 8 characters long"
            })
        elif re.search('[0-9]', password) is None:
            return render(request, "tttwars/register.html", {
                "message": "Password must have at least 1 number in it"
            })
        if password != confirmation:
            return render(request, "tttwars/register.html", {
                "message": "Passwords must match"
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "tttwars/register.html", {
                "message": "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tttwars/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Backend checking to make sure fields are filled out
        if username == "" or password == "":
            return render(request, "tttwars/register.html", {
                "message": "All fields must be filled out"
            })

        user = authenticate(request, username=username, password=password)

        # Checking if user exists
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tttwars/login.html", {
                "message": "Invalid email and/or password"
            })
    else:
        return render(request, "tttwars/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
