from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="BlogHome"),
    path("login/", views.login, name="BlogLogin"),
    path("logout/", views.logout, name="BlogLogout"),
    path("register/", views.register, name="BlogRegister"),
    path("dashboard/", views.dashboard, name="UserDashboard"),
    path("dashboard/changename/", views.changename, name="ChangeName"),
    path("dashboard/changeusername/", views.changeusername, name="ChangeUsername"),
    path("dashboard/changepassword/", views.changepassword, name="ChangePassword"),
    path("comments/post/", views.post_comment, name="PostComment"),
    path("comments/delete/", views.delete_comment, name="DeleteComment"),
    path("posts/like/", views.like_post, name="LikePost"),
    path("search/", views.search, name="BlogSearch"),
    path("tags/<str:tag>/", views.tag, name="TagSearch"),
    path("<str:slug>/", views.blogpost, name="BlogPost"),
]
