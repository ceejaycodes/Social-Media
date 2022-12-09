from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("viewpost/<int:id>", views.view_post, name="viewpost"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("addfollower/<int:id>", views.addfollower, name="addfollower"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following", views.following_posts, name="following")
    
    
]
