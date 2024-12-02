from django.urls import path
from . import views


urlpatterns = [
	#path('posts/',views.CommentsList.as_view(),name='posts'),
	#path('posts/<int:pk>/',views.CommentsDetail.as_view(),name='post-detail'),
    path('search/', views.search_filter, name='search'),
    path('user-profile/<int:id>/', views.user_profile, name='user-profile'),
    path('follow/', views.follow_user, name='follow-user'),
    path('follow-status/', views.follow_status, name='follow-status'),
    path('followed-profiles/', views.followed_profiles, name='followed-profiles'),
    path('profile-followers/', views.profile_followers, name='profile-followers'),
]