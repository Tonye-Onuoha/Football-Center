from django.urls import path
from . import views


urlpatterns = [
	path('posts/',views.CommentsList.as_view(),name='posts'),
	path('posts/<int:pk>/',views.CommentsDetail.as_view(),name='post-detail'),
]