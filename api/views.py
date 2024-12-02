from rest_framework import status
from django.contrib.auth.models import User
from football.models import Profiles
from api.serializers import UserSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

# Create your views here.
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def search_filter(request):
    """
    A view that returns the list of queried users in JSON.
    """
    if request.method == "GET":
        search_query = request.query_params.get("user_query").strip()
        users_list = search_query and User.objects.filter(
            Q(username__startswith=search_query)
            | Q(first_name__startswith=search_query)
            | Q(last_name__startswith=search_query)
        )
        if users_list:
            serializer = UserSerializer(users_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "user does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def user_profile(request, id):
    """
    A view that returns the details of a particular user in JSON format.
    """
    if request.method == "GET":
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(
                {"message": "user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            serializer = UserSerializer(user)
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            username = serializer.data["username"]
            profile = serializer.data["profile"]
            following = user.profile.followed_users.all().count()
            followers = user.profile_followers_set.all().count()
            data = {
                "id": id,
                "first_name":first_name,
                "last_name":last_name,
                "username":username,
                "profile":profile,
                "following":following,
                "followers":followers,
            }
            return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def follow_status(request):
    """
    A view that checks if the current logged-in user is following a particular profile.
    """
    if request.method == "GET":
        current_user_username = request.query_params.get("current_user")
        profile_user_username = request.query_params.get("profile_user")
        # get the user-object of the current user.
        current_user = User.objects.get(username=current_user_username)
        # confirm if the current user follows a particular profile via it's username.
        is_following = current_user.profile.followed_users.filter(
            username=profile_user_username
        ).exists()
        return Response({"is_following": is_following}, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def follow_user(request):
    """
    A view that enables the current user to follow or unfollow a profile.
    """
    if request.method == "GET":
        current_user_username = request.query_params.get("current_user")
        profile_user_username = request.query_params.get("profile_user")
        action = request.query_params.get("action")
        try:
            # get the user-object of the profile user.
            profile_user = User.objects.get(username=profile_user_username)
            # get the profile-object of the current user.
            current_user_profile = Profiles.objects.get(
                user__username=current_user_username
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "This user does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Profiles.DoesNotExist:
            return Response(
                {"status": "error", "message": "This profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            if action == "follow":
                current_user_profile.followed_users.add(profile_user)
                current_user_profile.save()
            elif action == "unfollow":
                current_user_profile.followed_users.remove(profile_user)
                current_user_profile.save()
        finally:
            return Response({"status": "success"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def followed_profiles(request):
    """
    A view that returns the users that a particular user follows in JSON format.
    """
    if request.method == "GET":
        user_username = request.query_params.get("user")
        # get the user-object of the current user.
        user = User.objects.get(username=user_username)
        # get the users the current user follows.
        followed_users = user.profile.followed_users.all()
        # serialize the queryset.
        serializer = UserSerializer(followed_users, many=True)
        # return a JSON response.
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def profile_followers(request):
    """
    A view that returns the followers of a particular user in JSON format.
    """
    if request.method == "GET":
        user_username = request.query_params.get("user")
        # get the user-object of the current user.
        user = User.objects.get(username=user_username)
        # get the followers of the current user.
        profile_followers = user.profile_followers_set.all()
        # get the user-object of each profile using list-comprehension.
        users_list = [profile.user for profile in profile_followers]
        # serialize the queryset.
        serializer = UserSerializer(users_list, many=True)
        # return a JSON response.
        return Response(serializer.data, status=status.HTTP_200_OK)
        
