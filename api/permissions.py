from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
	def has_permission(self,request,view):
		return True
	
	def has_object_permission(self,request,view,obj):
		if obj.author == request.user:
			return True