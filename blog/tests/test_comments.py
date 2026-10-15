from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Comment


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter',
            password='testpassword123'
        )
        self.post = Post.objects.create(
            title='Mountain Sunrise',
            slug='mountain-sunrise',
            author=self.user,
            category='landscape',
            excerpt='Sunrise over the misty peaks.',
            content='Full story of mountain sunrise.',
            status=2,
            location='Dolomites'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            name='Alice Smith',
            email='alice@example.com',
            body='Incredible photography! Love the lighting here.',
            approved=False
        )
        self.assertEqual(comment.post, self.post)
        self.assertFalse(comment.approved)
        self.assertEqual(self.post.number_of_comments(), 0)

    def test_comment_approval_and_count(self):
        comment = Comment.objects.create(
            post=self.post,
            name='Bob',
            email='bob@example.com',
            body='Great composition and colors.',
            approved=True
        )
        self.assertEqual(self.post.number_of_comments(), 1)

    def test_comment_str_truncation(self):
        short_comment = Comment.objects.create(
            post=self.post,
            name='Charlie',
            email='charlie@example.com',
            body='Nice shot!',
            approved=True
        )
        self.assertEqual(str(short_comment), 'Comment "Nice shot!" by Charlie')

        long_comment = Comment.objects.create(
            post=self.post,
            name='Dave',
            email='dave@example.com',
            body='This is an extraordinarily detailed review of a photo that spans over forty characters easily.',
            approved=True
        )
        self.assertTrue(str(long_comment).endswith('..." by Dave'))
