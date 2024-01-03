from django.contrib.auth.models import User
from .models import Profile, Replies, Quotes, Notification
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created == True:
        Profile.objects.create(user=instance)
        print("New Profile Created")


@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwargs):
    if created == False or created == None:
        instance.profile.save()
        print("User Profile Updated")

@receiver(post_save,sender=Replies)
def reply_notification(sender,instance,created,**kwargs):
	if created:
		# checks if this is a reply to a post or a quote
		if instance.comment:
			user = instance.comment.author
			message = instance
			reply_url = instance.get_absolute_url()
		else:
			user = instance.quote.user
			message = instance
			reply_url = instance.get_absolute_url()
		Notification.objects.create(user=user,reply=message,link=reply_url)

@receiver(post_save,sender=Quotes)
def quote_notification(sender,instance,created,**kwargs):
	if created:
		user = instance.post.author
		message = instance
		quote_url = instance.get_absolute_url()
		Notification.objects.create(user=user,quote=message,link=quote_url)
		
		
