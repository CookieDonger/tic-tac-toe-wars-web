from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("play", views.play, name="play"),
    path("createroom", views.create_room, name="createroom"),
    path("<int:room_id>", views.room, name="room"),
    path("leave/<int:room_id>", views.leave_game, name="leave"),
    path("resign/<int:room_id>", views.resign, name="resign"),
    path("friends", views.friends, name="friends"),
    path("history", views.history, name="history"),
    path("history/<int:game_id>", views.history_game, name="historygame"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    # API Routes
    path("profile/<str:username>", views.profile, name="profile"),
    path("profiles/<int:user_id>", views.get_profile, name="getprofile"),
    path("profiles/<str:username>", views.get_profile2, name="getprofile2"),
    path("getroom/<int:game_id>", views.get_room, name="getroom"),
    path("startgame/<int:game_id>", views.start_game, name="startgame"),
    path("playmove/<int:game_id>", views.play_move, name="playmove")
]
