from django.urls import path
from .auth_views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="regitser"),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    # Profile
    path("profiles/", ProfileView.as_view(), name="profiles"),
    path("profiles/<int:pk>/", ProfileView.as_view(), name="profile_detail"),
    path(
        "profiles/<int:pk>/follow/",
        FollowUnfollowView.as_view(),
        name="follow"),
    # Posts
    path("posts/", PostView.as_view(), name="posts"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/like/", LikeUnlikeView.as_view(), name="like_post"),
    # Comments
    path(
        "posts/<int:pk>/comments/",
        CommentView.as_view(),
        name="post_comments"),
    path(
        "comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail"),
    # Feed
    path("feed/", FeedView.as_view(), name="feed"),
]
