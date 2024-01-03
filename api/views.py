from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from football.models import Comments
from api.serializers import CommentsSerializer
from rest_framework import permissions
from .permissions import IsAuthor

# Create your views here.

class CommentsList(ListCreateAPIView):
	queryset = Comments.objects.all()
	serializer_class = CommentsSerializer
	permission_classes = (IsAuthor,)
	
	def perform_create(self,serializer):
		serializer.save(author=self.request.user)
		
		
class CommentsDetail(RetrieveUpdateDestroyAPIView):
	queryset = Comments.objects.all()
	serializer_class = CommentsSerializer
	permission_classes = (IsAuthor,)
	
	

