from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.forms import CommentForm, PostForm


class FormValidationTests(TestCase):
    def test_comment_form_valid(self):
        form = CommentForm(data={'body': 'This is a genuine comment.'})
        self.assertTrue(form.is_valid())

    def test_comment_form_blank_body_invalid(self):
        form = CommentForm(data={'body': '   '})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_post_form_title_too_short(self):
        form = PostForm(data={
            'title': 'Hi',
            'category': 'travel',
            'excerpt': 'Valid excerpt here',
            'location': 'Tokyo',
            'content': 'Valid content here',
            'status': 0,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_post_form_invalid_image_extension(self):
        fake_file = SimpleUploadedFile(
            'document.pdf',
            b'dummy file content',
            content_type='application/pdf'
        )
        form = PostForm(
            data={
                'title': 'Valid Title Here',
                'category': 'travel',
                'excerpt': 'Valid excerpt here',
                'location': 'Tokyo',
                'content': 'Valid content here',
                'status': 0,
            },
            files={'featured_image': fake_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('featured_image', form.errors)
