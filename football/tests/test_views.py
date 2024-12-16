from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from football.models import Comments, Replies, Quotes, Notifications
from django.urls import reverse

# Create your tests here.
class RegisterViewTest(TestCase):
    """This subclass tests the view responsible for handling the user-registration."""
    def test_get_register_form(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_post_register_form(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTemplateUsed(response, "registration/register.html")
        data = {
            "username": "jane",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@gmail.com",
            "password1": "sBQl6fk085",
            "password2": "sBQl6fk085",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class CreatePostViewTest(TestCase):
    """This subclass tests the view responsible for handling the creation of new comments/posts."""
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )

    def test_get_create_post_form(self):
        login = self.client.login(username="john", password="zGXn9dk143")
        response = self.client.get(reverse("create-post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_post.html")

    def test_create_new_post(self):
        login = self.client.login(username="john", password="zGXn9dk143")
        response = self.client.post(
            reverse("create-post"), {"post": "This is my first post."}
        )
        self.assertEqual(response.status_code, 302)


class EditPostViewTest(TestCase):
    """This subclass tests the view responsible for handling post edits."""
    def setUp(self):
        self.user = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        self.post = Comments.objects.create(
            post="This is a new post.", author=self.user
        )

    def test_get_update_post(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # GET-request method
        no_response = self.client.get(reverse("edit-post", args=[100]))
        self.assertEqual(no_response.status_code, 404)
        response = self.client.get(reverse("edit-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTemplateUsed(response, "edit.html")

    def test_post_update_post(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # edit a post
        no_response = self.client.get(reverse("edit-post", args=[100]))
        self.assertEqual(no_response.status_code, 404)
        response = self.client.get(reverse("edit-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTemplateUsed(response, "edit.html")
        # update a post
        data = {"post": "This is an updated post."}
        response = self.client.post(reverse("edit-post", args=[self.post.id]), data)
        self.assertEqual(response.status_code, 302)


class DeletePostViewTest(TestCase):
    """This subclass tests the view responsible for handling the deletion of comments/posts."""
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        self.post = Comments.objects.create(post="This is a new post", author=self.user)

    def test_delete_post(self):
        # log in user
        login = self.client.login(username="john", password="zGXn9dk143")
        # GET-request method
        no_response = self.client.get(reverse("delete-post", args=[100]))
        self.assertEqual(no_response.status_code, 404)
        response = self.client.get(reverse("delete-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")
        # POST-request method
        response = self.client.post(reverse("delete-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 302)


class ReplyPostViewTest(TestCase):
    """This subclass tests the view responsible for handling poat replies."""
    def setUp(self):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        self.post = Comments.objects.create(post="This is a new post", author=user_1)

    def test_get_reply_form(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # GET-request method
        response = self.client.get(reverse("reply-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("post" in response.context)
        self.assertTemplateUsed(response, "reply_form.html")

    def test_post_reply_form(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # POST-request method
        data = {"reply": "I have replied your post"}
        response = self.client.post(reverse("reply-post", args=[self.post.id]), data)
        self.assertEqual(response.status_code, 302)


class QuotePostViewTest(TestCase):
    """This subclass tests the view responsible for handling post quotes."""
    def setUp(self):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        self.post = Comments.objects.create(post="This is a new post", author=user_1)

    def test_get_quote_form(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # GET-request method
        response = self.client.get(reverse("quote-post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("post" in response.context)
        self.assertTemplateUsed(response, "quote_form.html")

    def test_post_quote_form(self):
        # log in user
        login = self.client.login(username="jane", password="sBQl6fk085")
        # POST-request method
        data = {"quote": "I have quoted your post"}
        response = self.client.post(reverse("quote-post", args=[self.post.id]), data)
        self.assertEqual(response.status_code, 302)


class NotificationsViewTest(TestCase):
    """This subclass tests the view responsible for handling users notifications."""
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        post = Comments.objects.create(post="This is a new post", author=user_1)
        Replies.objects.create(reply="A reply to your post", comment=post, user=user_2)

    def test_get_all_notifications(self):
        # log in user
        login = self.client.login(username="john", password="zGXn9dk143")
        # GET-request method
        response = self.client.get(reverse("user-notifications-new"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("notifications" in response.context)
        self.assertTemplateUsed(response, "notifications.html")
