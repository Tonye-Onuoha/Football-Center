from django.contrib.auth.models import User
from .models import Profiles, Replies, Quotes, Notifications
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    A function that automatically creates a new profile for each newly created user.
    """
    if created == True:
        Profiles.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    """
    A function that updates a user's profile when the user is updated.
    """
    if created == False or created == None:
        if hasattr(instance, "profile"):
            instance.profile.save()


@receiver(post_save, sender=Replies)
def reply_notification(sender, instance, created, **kwargs):
    """
    A function that automatically creates a reply-notification when someone replies to a user's post/quote.
    """
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
        Notifications.objects.create(user=user, reply=message, link=reply_url)


@receiver(post_save, sender=Quotes)
def quote_notification(sender, instance, created, **kwargs):
    """
    A function that automatically creates a quote-notification when someone quotes a user's post.
    """
    if created:
        user = instance.post.author
        message = instance
        quote_url = instance.get_absolute_url()
        Notifications.objects.create(user=user, quote=message, link=quote_url)
