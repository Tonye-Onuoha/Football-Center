from rest_framework import serializers
from football.models import Comments


class CommentsSerializer(serializers.ModelSerializer):
	author = serializers.StringRelatedField(read_only=True)
	
	class Meta:
		model = Comments
		fields = ['id','post','author','date']