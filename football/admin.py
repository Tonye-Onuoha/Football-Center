from django.contrib import admin
from .models import Comments, League, Club, Players, Profile, Replies, Quotes, Notification

# Register your models here.
admin.site.register(Comments)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Players)
admin.site.register(Profile)
admin.site.register(Replies)
admin.site.register(Quotes)
admin.site.register(Notification)
