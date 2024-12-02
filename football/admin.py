from django.contrib import admin
from .models import Comments, League, Club, Players, Profiles, Replies, Quotes, Notifications

# Register your models here.
admin.site.register(Comments)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Players)
admin.site.register(Profiles)
admin.site.register(Replies)
admin.site.register(Quotes)
admin.site.register(Notifications)
