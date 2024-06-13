from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from football.models import Comments,Replies,Quotes,Notification
from django.urls import reverse

# Create your tests here.
class HomeViewTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        
        
    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/accounts/login/?next=/')
        
    def test_user_logged_in(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'john')
        
    def test_correct_template_used(self):
        login = self.client.login(username='jane',password='sBQl6fk085')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'jane')
        self.assertTemplateUsed(response,'home.html')
       
    
class HomeViewPostTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        comment = Comments.objects.create(post='This is a new post',author=user_1)
        
    def test_post_exists(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'john')
        self.assertTemplateUsed(response,'home.html')
        self.assertContains(response,'This is a new post')
        # Check if posts exist
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']),1)
        
class HomeViewQuoteTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        comment = Comments.objects.create(post='This is a new post',author=user_1)
        quote = Quotes.objects.create(quote='I just quoted your post',post=comment,user=user_2)
        
    def test_quote_exists(self):
        login = self.client.login(username='jane',password='sBQl6fk085')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'jane')
        # Check if posts exist
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']),2)
        
        
class HomeViewNotificationsTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        comment = Comments.objects.create(post='This is a new post',author=user_1)
        Quotes.objects.create(quote='I just quoted your post',post=comment,user=user_2)
        
    def test_notification_exists(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'john')
        # Check if notifications exist
        self.assertTrue('notifications_count' in response.context)
        self.assertTrue(response.context['notifications_count'] > 0)
        
class HomeViewMultiplePostsTests(TestCase):
    def setUp(self):
        # Create two users
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        # Create four posts
        Comments.objects.create(post='This is my first post',author=user_1)
        Comments.objects.create(post='This is my first post',author=user_2)
        Comments.objects.create(post='This is my second post',author=user_1)
        Comments.objects.create(post='This is my second post',author=user_2)
        
    def test_posts_ordered_by_date_and_time(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('user' in response.context)
        self.assertEqual(str(response.context['user']),'john')
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']),4)
        
        # Confirm posts are ordered by date
        latest_post_date = 0
        for post in response.context['posts']:
            if latest_post_date == 0:
                latest_post_date = post.date
            else:
                self.assertTrue(latest_post_date > post.date)
                lastest_post_date = post.date
                
                
class RegisterViewTest(SimpleTestCase):
    def test_get_register_form(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response,'register.html')
        
    def test_post_register_form(self):
        response = self.client.get('register')
        self.assertEqual(response.status_code,200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response,'register.html')
        response = self.client.post(reverse('register'),{'username':'jane','password':'sBQl6fk085','email':'janedoe@gmail.com','first_name':'Jane','last_name':'Doe'})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))
        
class CreatePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        
    def test_get_create_post_form(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.get(reverse('create-post'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'create_post.html')
        
    def test_post_create_post_form(self):
        login = self.client.login(username='john',password='zGXn9dk143')
        response = self.client.post(reverse('create-post'),{'post':'This is my first post',author:self.user})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
        
class EditPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        self.post = Comments.objects.create(post='This is a new post',author=self.user)
        
    def test_get_update_post(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # get request method
        response = self.client.get(reverse('edit-post', args=self.post.id))
        no_reponse = self.client.get(reverse('edit-post', args='100'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response,'edit.html')
        
    def test_post_update_post(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # Edit a post
        response = self.client.get(reverse('edit-post', args=self.post.id))
        no_reponse = self.client.get(reverse('edit-post', args='100'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response,'edit.html')
        # Update a post
        response = self.client.post(reverse('edit-post',args=self.post.id),{'post':'This is an updated post'})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
        
class DeletePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        self.post = Comments.objects.create(post='This is a new post',author=self.user)
        
    def test_delete_post(self):
        # log in user
        login = self.client.login(username='john',password='zGXn9dk143')
        # get request method
        response = self.client.get(reverse('delete-post'),args=self.post.id)
        no_reponse = self.client.get(reverse('delete-post', args='100'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTemplateUsed(response,'delete.html')
        # post request method
        response = self.client.post(reverse('delete-post',args=self.post.id))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
        
class ReplyPostViewTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        self.post = Comments.objects.create(post='This is a new post',author=user_1)
        
    def test_get_reply_form(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # get request method
        response = self.client.get(reverse('reply-post',args=self.post.id))
        self.assertEqual(response.status_code,200)
        self.assertTrue('form' in response.context)
        self.assertTrue('post' in response.context)
        self.assertTemplateUsed(response,'reply_form.html')
        
    def test_post_reply_form(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # post request method
        response = self.client.post(reverse('reply-post',args=self.post.id),{'reply':'I have replied your post'})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
        
        
class QuotePostViewTest(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        self.post = Comments.objects.create(post='This is a new post',author=user_1)
        
    def test_get_quote_form(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # get request method
        response = self.client.get(reverse('quote-post',args=self.post.id))
        self.assertEqual(response.status_code,200)
        self.assertTrue('form' in response.context)
        self.assertTrue('post' in response.context)
        self.assertTemplateUsed(response,'quote_form.html')
        
    def test_post_quote_form(self):
        # log in user
        login = self.client.login(username='jane',password='sBQl6fk085')
        # post request method
        response = self.client.post(reverse('quote-post',args=self.post.id),{'quote':'I have quoted your post'})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
        
class NotificationsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(username='john',email='johndoe@gmail.com',password='zGXn9dk143')
        user_2 = User.objects.create_user(username='jane',email='janedoe@gmail.com',password='sBQl6fk085')
        post = Comments.objects.create(post='This is a new post',author=user_1)
        Replies.objects.create(reply='A reply to your post',comment=post,user=user_2)
        
    def test_get_all_notifications(self):
        # log in user
        login = self.client.login(username='john',password='zGXn9dk143')
        # get request method
        response = self.client.get(reverse('user-notifications'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('notifications' in response.context)
        self.assertTemplateUsed(response,'notifications.html')
        
        
        
        
        
    
        
        
        
        
        
                             
                    
        