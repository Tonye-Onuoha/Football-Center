from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.
class Comments(models.Model):
	post = models.TextField(help_text="Enter a post",blank=False)
	author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name="Author")
	date = models.DateTimeField(auto_now_add=True,null=True)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.author.username

class Replies(models.Model):
	reply = models.TextField(help_text='Enter a comment',max_length=200)
	comment = models.ForeignKey(Comments,on_delete=models.CASCADE,blank=True,null=True)
	quote = models.ForeignKey('Quotes',on_delete=models.CASCADE,blank=True,null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['id']

	def get_absolute_url(self):
		return reverse('reply-detail',args=[str(self.id)])

	def __str__(self):
		return self.user.username

class Quotes(models.Model):
	quote = models.TextField(help_text='quote this post',max_length=150,blank=False)
	post = models.ForeignKey(Comments,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['id']

	def get_absolute_url(self):
		return reverse('quote-detail',args=[str(self.id)])

	def __str__(self):
		return f'{self.user} quote {self.id}'

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default="avatar.png", upload_to="profile_pics/")
	bio = models.TextField(help_text='Tell us about yourself', max_length=100, blank=True, null=True)
	
	class Meta:
		ordering = ['id']
		
	"""def save(self, *args, **kwargs):
		# save the profile first
		super().save(*args, **kwargs)
		
		# resize the image
		img = Image.open(self.image.path)
		if img.height > 400 or img.width > 400:
			output_size = (400, 400)
			# create a thumbnail
			img.thumbnail(output_size)
			# overwrite the larger image
			img.save(self.image.path)"""
			
	def __str__(self):
		return "{} Profile".format(self.user.username)

class Notification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	reply = models.ForeignKey(Replies,on_delete=models.CASCADE,blank=True,null=True)
	quote = models.ForeignKey(Quotes,on_delete=models.CASCADE,blank=True,null=True)
	link = models.URLField(max_length=30)
	read = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('notification-detail',args=[str(self.id)])

	def __str__(self):
		return "{}'s notification".format(self.user)

class Club(models.Model):
    name = models.CharField(max_length=25,unique=True)
    league = models.ForeignKey('League',on_delete=models.CASCADE)
    description = models.TextField(help_text="Club Description",null=True,blank=True)
    logo = models.ImageField(blank=True,null=True,upload_to="club_logos/")
    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('club-details',args=[str(self.id)])

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=25,unique=True,null=False)
    country = models.CharField(max_length=30)
    description = models.TextField(null=True,blank=True)
    logo = models.ImageField(blank=True,null=True,upload_to="league_logos/")
    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('league-details',args=[str(self.id)])

    def __str__(self):
        return self.name

class Players(models.Model):
    name = models.CharField(help_text="Enter player name",max_length=30)
    club = models.ForeignKey(Club,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(blank=True,null=True,default='footballer_icon',upload_to="players_images/")
    profile = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['club','name']

    def get_absolute_url(self):
        return reverse('player-details',args=[str(self.id)])

    def __str__(self):
        return self.name