from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class User(AbstractUser):
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    rating = models.PositiveIntegerField(default=1000, validators=[MinValueValidator(1), MaxValueValidator(5000)])

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "datejoined": self.date_joined.strftime('%m %d, %Y'),
            "rating": self.rating,
            "friends": [user.username for user in self.friends.all()],
            "requested": [request.requestor.username for request in self.requested.all()],
        }


class FriendRequest(models.Model):
    requestor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requestor')
    requested = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requested')


class TTTWarsGame(models.Model):
    players = models.ManyToManyField('User', related_name='players')
    p1 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='offense', blank=True, null=True)
    p2 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='defense', blank=True, null=True)
    p1rating = models.IntegerField(default=0)
    p2rating = models.IntegerField(default=0)
    winner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
    active = models.BooleanField(default=True)
    started = models.BooleanField(default=False)
    board1 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    board2 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    board3 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    board4 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    board5 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    board6 = models.JSONField(default=list((list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)), list((0, 0, 0, 0, 0, 0)))))
    movecount = models.IntegerField(default=0)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    p1game1score = models.IntegerField(default=0)
    p2game1score = models.IntegerField(default=0)
    p1game2score = models.IntegerField(default=0)
    p2game2score = models.IntegerField(default=0)
    p1game3score = models.IntegerField(default=0)
    p2game3score = models.IntegerField(default=0)
    p1game4score = models.IntegerField(default=0)
    p2game4score = models.IntegerField(default=0)
    p1game5score = models.IntegerField(default=0)
    p2game5score = models.IntegerField(default=0)
    p1game6score = models.IntegerField(default=0)
    p2game6score = models.IntegerField(default=0)
    matchscore1 = models.IntegerField(default=0)
    matchscore2 = models.IntegerField(default=0)
    gamenumber = models.IntegerField(default=1)

    # So I can't access the username variable if the object doesn't exist, and I can't return an object for
    # serialization, thus I'm going to use a boolean to check if the object exists
    def serialize(self):
        if self.p1:
            p1 = self.p1.username
        else:
            p1 = "None"
        if self.p2:
            p2 = self.p2.username
        else:
            p2 = "None"
        if self.winner:
            winner = self.winner.username
        else:
            winner = "None"
        return {
            "id": self.id,
            "players": [user.username for user in self.players.all()],
            "p1": p1,
            "p1rating": self.p1rating,
            "p2rating": self.p2rating,
            "p2": p2,
            "winner": winner,
            "active": self.active,
            "started": self.started,
            "board1": self.board1,
            "board2": self.board2,
            "board3": self.board3,
            "board4": self.board4,
            "board5": self.board5,
            "board6": self.board6,
            "movecount": self.movecount,
            "score1": self.score1,
            "score2": self.score2,
            "p1game1score": self.p1game1score,
            "p2game1score": self.p2game1score,
            "p1game2score": self.p1game2score,
            "p2game2score": self.p2game2score,
            "p1game3score": self.p1game3score,
            "p2game3score": self.p2game3score,
            "p1game4score": self.p1game4score,
            "p2game4score": self.p2game4score,
            "p1game5score": self.p1game5score,
            "p2game5score": self.p2game5score,
            "p1game6score": self.p1game6score,
            "p2game6score": self.p2game6score,
            "matchscore1": self.matchscore1,
            "matchscore2": self.matchscore2,
            "gamenumber": self.gamenumber
        }
