from django.test import SimpleTestCase
from football.forms import RegisterForm,PostForm,ReplyPostForm,QuoteForm,ProfileUpdateForm

# Create your tests here.
class RegisterFormTest(SimpleTestCase):
    def test_username_label(self):
        form = RegisterForm()
        label = form.fields['username'].label
        self.assertTrue(label == None or label == 'Username')
        
    def test_email_label(self):
        form = RegisterForm()
        label = form.fields['email'].label
        self.assertTrue(label == None or label == 'email')
        
    def test_first_name_label(self):
        form = RegisterForm()
        label = form.fields['first_name'].label
        self.assertTrue(label == None or label == 'first name')
        
    def test_last_name_label(self):
        form = RegisterForm()
        label = form.fields['last_name'].label
        self.assertTrue(label == None or label == 'last name')
        
class PostFormTest(SimpleTestCase):
    def test_post_label(self):
        form = PostForm()
        label = form.fields['post'].label
        self.assertTrue(label == None or label == '')
    
class ReplyPostFormTest(SimpleTestCase):
    def test_reply_label(self):
        form = ReplyPostForm()
        label = form.fields['reply'].label
        self.assertTrue(label == None or label == '')
    
class QuoteFormTest(SimpleTestCase):
    def test_quote_label(self):
        form = QuoteForm()
        label = form.fields['quote'].label
        self.assertTrue(label == None or label == '')
        
class ProfileUpdateFormTest(SimpleTestCase):
    def test_bio_label(self):
        form = ProfileUpdateForm()
        label = form.fields['bio'].label
        self.assertTrue(label == None or label == 'Bio')
        
    def test_image_label(self):
        form = ProfileUpdateForm()
        label = form.fields['image'].label
        self.assertTrue(label == None or label == 'Image')
        
    
    
        
        