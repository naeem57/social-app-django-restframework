from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Profile, Post, Like, Comment, Notification
from .serializers import *


# ------------------ PROFILE ------------------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Return the logged-in user's profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(
            {"msg": "Profile fetched successfully", "data": serializer.data}
        )

    def post(self, request):
        # Prevent creating multiple profiles
        if hasattr(request.user, "profile"):
            return Response(
                {"error": "Profile already exists. Use PUT to update."}, status=400
            )

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"msg": "Profile created", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        # Update only the user's own profile
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Profile updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        return Response({"msg": "Profile deleted successfully"})


# ------------------ FOLLOW / UNFOLLOW ------------------
class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user = request.user

        if profile.user == user:
            return Response({"error": "You can't follow yourself"}, status=400)

        if user in profile.followers.all():
            profile.followers.remove(user)
            return Response({"message": "Unfollowed"})
        else:
            profile.followers.add(user)
            return Response({"message": "Followed"})


# ------------------ POSTS ------------------
class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"msg": "Post created", "data": serializer.data})
        return Response(serializer.errors, status=400)


class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({"data": serializer.data})

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"error": "You can only edit your own post"}, status=403)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Post updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"error": "You can only delete your own post"}, status=403)
        post.delete()
        return Response({"msg": "Post deleted"})


# ------------------ LIKE / UNLIKE ------------------
class LikeUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"})
        Notification.objects.create(
            sender=request.user,
            receiver=post.author,
            message=f"{request.user.username} liked your post.",
        )
        return Response({"message": "Liked"})


# ------------------ COMMENT ------------------
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text is required"}, status=400)
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        Notification.objects.create(
            sender=request.user,
            receiver=post.author,
            message=f"{request.user.username} commented on your post.",
        )
        return Response(CommentSerializer(comment).data)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response({"error": "You can only edit your own comment"}, status=403)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Comment updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response(
                {"error": "You can only delete your own comment"}, status=403
            )
        comment.delete()
        return Response({"msg": "Comment deleted"})


# ------------------ FEED ------------------
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()
        posts = Post.objects.filter(author__in=following).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response({"data": serializer.data})
