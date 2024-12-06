from django.test import TestCase
from football.models import Comments, Replies, Quotes, Notifications
from django.contrib.auth.models import User

# Create your tests here.
class CommentsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        post = Comments(post="My first post", author=user)
        post.save()

    def test_post_label(self):
        comment = Comments.objects.filter(post__contains="My").first()
        post_label = comment._meta.get_field("post").verbose_name
        self.assertEqual(post_label, "post")

    def test_post_help_text(self):
        comment = Comments.objects.all().first()
        post_help_text = comment._meta.get_field("post").help_text
        self.assertEqual(post_help_text, "Enter a post.")

    def test_author_label(self):
        comment = Comments.objects.all().first()
        author_label = comment._meta.get_field("author").verbose_name
        self.assertEqual(author_label, "Author")

    def test_post_author(self):
        comment = Comments.objects.all().first()
        expected_user = "john"
        self.assertEqual(comment.author.username, expected_user)

    def test_post_content(self):
        comment = Comments.objects.get(id=1)
        self.assertEqual(f"{comment.post}", "My first post")

    def test_queryset(self):
        queryset = Comments.objects.all()
        expected_size = 1
        self.assertEqual(len(queryset), expected_size)

    def test_string_method(self):
        comment = Comments.objects.get(id=1)
        self.assertEqual(str(comment), "john")


class RepliesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        post = Comments(post="I love football", author=user_1)
        post.save()
        Replies.objects.create(
            reply="I replied to your post", comment=post, user=user_2
        )

    def test_reply_label(self):
        reply = Replies.objects.get(id=1)
        label = reply._meta.get_field("reply").verbose_name
        self.assertEqual(label, "reply")

    def test_help_text(self):
        reply = Replies.objects.get(id=1)
        help_text = reply._meta.get_field("reply").help_text
        self.assertEqual(help_text, "Enter a comment.")

    def test_max_length(self):
        reply = Replies.objects.get(id=1)
        max_length = reply._meta.get_field("reply").max_length
        self.assertEqual(max_length, 200)

    def test_post_user(self):
        reply = Replies.objects.get(id=1)
        expected_username = "john"
        self.assertEqual(reply.comment.author.username, expected_username)

    def test_reply_user(self):
        reply = Replies.objects.get(id=1)
        expected_username = "jane"
        self.assertEqual(reply.user.username, expected_username)

    def test_reply_content(self):
        reply = Replies.objects.get(id=1)
        expected_reply = "I replied to your post"
        self.assertEqual(f"{reply.reply}", expected_reply)

    def test_queryset(self):
        queryset = Replies.objects.all()
        expected_size = 1
        self.assertEqual(len(queryset), expected_size)

    def test_get_absolute_url(self):
        reply = Replies.objects.all().first()
        expected_url = "/post-reply/1/"
        self.assertEqual(reply.get_absolute_url(), expected_url)

    def test_string_method(self):
        reply = Replies.objects.all().first()
        self.assertEqual(str(reply), "jane")


class QuotesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        post = Comments.objects.create(post="This is a new post", author=user_1)
        Quotes.objects.create(
            quote="I just quoted your post", post=post, user=user_2
        )

    def test_quote_label(self):
        quote = Quotes.objects.get(id=1)
        label = quote._meta.get_field("quote").verbose_name
        self.assertEqual(label, "quote")

    def test_help_text(self):
        quote = Quotes.objects.get(id=1)
        help_text = quote._meta.get_field("quote").help_text
        self.assertEqual(help_text, "Quote this post.")

    def test_max_length(self):
        quote = Quotes.objects.get(id=1)
        max_length = quote._meta.get_field("quote").max_length
        self.assertEqual(max_length, 150)

    def test_post_user(self):
        quote = Quotes.objects.get(id=1)
        expected_username = "john"
        self.assertEqual(quote.post.author.username, expected_username)

    def test_quote_user(self):
        quote = Quotes.objects.get(id=1)
        expected_username = "jane"
        self.assertEqual(quote.user.username, expected_username)

    def test_quote_content(self):
        quote = Quotes.objects.get(id=1)
        expected_quote = "I just quoted your post"
        self.assertEqual(f"{quote.quote}", expected_quote)

    def test_queryset(self):
        queryset = Quotes.objects.all()
        expected_size = 1
        self.assertEqual(len(queryset), expected_size)

    def test_get_absolute_url(self):
        quote = Quotes.objects.all().first()
        expected_url = "/post-quote/1/"
        self.assertEqual(quote.get_absolute_url(), expected_url)

    def test_string_method(self):
        quote = Quotes.objects.all().first()
        expected_string = "jane quote 1"
        self.assertEqual(str(quote), expected_string)


class NotificationsModelTest1(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        post = Comments.objects.create(post="I am writing a test", author=user_1)
        Replies.objects.create(
            reply="This is your first reply", comment=post, user=user_2
        )

    def test_notification_exists(self):
        notification = Notifications.objects.all()
        expected_size = 1
        self.assertEqual(len(notification), 1)

    def test_notification_owner(self):
        notification = Notifications.objects.get(id=1)
        expected_user = "john"
        self.assertEqual(f"{notification.user}", expected_user)

    def test_notification_is_reply(self):
        notification = Notifications.objects.get(id=1)
        self.assertFalse(bool(notification.quote))
        self.assertTrue(bool(notification.reply))

    def test_notification_link_url(self):
        notification = Notifications.objects.get(id=1)
        expected_url = "/post-reply/1/"
        self.assertEqual(f"{notification.link}", expected_url)

    def test_notification_unseen(self):
        notification = Notifications.objects.get(id=1)
        self.assertFalse(notification.read)

    def test_string_method(self):
        notification = Notifications.objects.get(id=1)
        expected_string = "john's notification"
        self.assertEqual(str(notification), expected_string)


class NotificationsModelTest2(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="zGXn9dk143"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="sBQl6fk085"
        )
        comment = Comments.objects.create(post="I am writing a test", author=user_1)
        Quotes.objects.create(
            quote="This is your first quote", post=comment, user=user_2
        )

    def test_notification_exists(self):
        notification = Notifications.objects.all()
        expected_size = 1
        self.assertEqual(len(notification), 1)

    def test_notification_owner(self):
        notification = Notifications.objects.get(id=1)
        expected_user = "john"
        self.assertEqual(f"{notification.user}", expected_user)

    def test_notification_is_quote(self):
        notification = Notifications.objects.get(id=1)
        self.assertFalse(bool(notification.reply))
        self.assertTrue(bool(notification.quote))

    def test_notification_link_url(self):
        notification = Notifications.objects.get(id=1)
        expected_url = "/post-quote/1/"
        self.assertEqual(f"{notification.link}", expected_url)

    def test_notification_unseen(self):
        notification = Notifications.objects.get(id=1)
        self.assertFalse(notification.read)

    def test_string_method(self):
        notification = Notifications.objects.get(id=1)
        expected_string = "john's notification"
        self.assertEqual(str(notification), expected_string)
