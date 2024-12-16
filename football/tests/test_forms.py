from django.test import SimpleTestCase
from football.forms import (
    RegisterForm,
    PostForm,
    ReplyPostForm,
    QuoteForm,
    ProfileUpdateForm,
)

# Create your tests here.
class RegisterFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for user-registration."""
    def test_username_label(self):
        form = RegisterForm()
        label = form.fields["username"].label
        self.assertTrue(label == None or label == "Username")

    def test_email_label(self):
        form = RegisterForm()
        label = form.fields["email"].label
        self.assertTrue(label == None or label == "email")

    def test_first_name_label(self):
        form = RegisterForm()
        label = form.fields["first_name"].label
        self.assertTrue(label == None or label == "first name")

    def test_last_name_label(self):
        form = RegisterForm()
        label = form.fields["last_name"].label
        self.assertTrue(label == None or label == "last name")


class PostFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for creating new posts."""
    def test_post_label(self):
        form = PostForm()
        label = form.fields["post"].label
        self.assertTrue(label == None or label == "")
        
    def test_post_help_text(self):
        form = PostForm()
        help_text = form.fields["post"].help_text
        self.assertEqual(help_text, "Enter a new post.")


class ReplyPostFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for replying to posts."""
    def test_reply_label(self):
        form = ReplyPostForm()
        label = form.fields["reply"].label
        self.assertTrue(label == None or label == "")
        
    def test_reply_help_text(self):
        form = ReplyPostForm()
        help_text = form.fields["reply"].help_text
        self.assertEqual(help_text, "Enter a reply.")
        
    def test_reply_max_length(self):
        form = ReplyPostForm()
        max_length = form.fields["reply"].max_length
        self.assertEqual(max_length, 150)


class QuoteFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for quoting existing posts."""
    def test_quote_label(self):
        form = QuoteForm()
        label = form.fields["quote"].label
        self.assertTrue(label == None or label == "")
        
    def test_quote_help_text(self):
        form = QuoteForm()
        help_text = form.fields["quote"].help_text
        self.assertEqual(help_text, "Enter a quote.")
        
    def test_quote_max_length(self):
        form = QuoteForm()
        max_length = form.fields["quote"].max_length
        self.assertEqual(max_length, 150)


class ProfileUpdateFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for updating users profiles."""
    def test_bio_label(self):
        form = ProfileUpdateForm()
        label = form.fields["bio"].label
        self.assertTrue(label == None or label == "Bio")

    def test_image_label(self):
        form = ProfileUpdateForm()
        label = form.fields["image"].label
        self.assertTrue(label == None or label == "Image")
