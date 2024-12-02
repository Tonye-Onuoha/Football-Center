from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('teams/',views.TeamList.as_view(),name='teams'),
    path('teams/<int:pk>/',views.team_details,name='club-details'),
    path('players/',views.PlayerList.as_view(),name='players'),
    path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player-details'),
    path('leagues/',views.LeagueList.as_view(),name='leagues'),
    path('league/<int:pk>/',views.league_details,name='league-details'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('create/',views.create_post,name='create-post'),
    path('edit/<int:pk>/',views.edit_post,name='edit-post'),
    path('delete/<int:pk>/',views.delete_post,name='delete-post'),
    path('reply-new/<int:id>/',views.reply_post,name='reply-post'),
    path('replies/<int:id>/',views.post_replies,name='post-replies'),
    path('post-reply/<int:id>/',views.post_reply_detail,name='reply-detail'),
	path('delete-reply/<int:id>/',views.reply_delete,name='reply-delete'),
    path('quote-new/<int:id>/',views.quote_post,name='quote-post'),
    path('quotes/<int:id>/',views.quotes_view,name='quotes-view'),
    path('post-quote/<int:id>/',views.post_quote_detail,name='quote-detail'),
	path('edit-quote/<int:id>/',views.edit_quote,name='edit-quote'),
	path('delete-quote/<int:id>/',views.delete_quote,name='delete-quote'),
	path('reply-quote/<int:id>/',views.reply_quote,name='reply-quote'),
	path('quote-replies/<int:id>/',views.quote_replies,name='quote-replies'),
    path('author-profile/<int:id>/',views.author_profile,name='author-profile'),
    path('notifications/new/',views.notifications_view_new,name='user-notifications-new'),
    path('notifications/all/',views.notifications_view_all,name='user-notifications-all'),
    path('followed-profiles/<str:username>/', views.followed_profiles, name='followed-profiles'),
    path('profile-followers/<str:username>/', views.profile_followers, name='profile-followers'),
]
