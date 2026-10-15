from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Comment


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testphotographer',
            password='testpassword123'
        )
        self.published_post = Post.objects.create(
            title='Sunset over the Alps',
            author=self.user,
            category='landscape',
            excerpt='A stunning view of alpine peaks during golden hour.',
            content='Lorem ipsum dolor sit amet. ' * 50,  # ~250 words
            status=2,
            featured=True,
            location='Swiss Alps'
        )
        self.draft_post = Post.objects.create(
            title='Draft in Progress',
            author=self.user,
            category='adventure',
            excerpt='Working draft notes.',
            content='Draft text',
            status=0,
            location='Munich'
        )

    def test_auto_slug_generation(self):
        self.assertEqual(self.published_post.slug, 'sunset-over-the-alps')
        self.assertEqual(self.draft_post.slug, 'draft-in-progress')

    def test_str_representation(self):
        self.assertEqual(str(self.published_post), 'Sunset over the Alps')

    def test_is_published_property(self):
        self.assertTrue(self.published_post.is_published)
        self.assertFalse(self.draft_post.is_published)

    def test_reading_time_calculation(self):
        # 50 repetitions of 5 words = 250 words -> round(250/200) = 1 min
        self.assertGreaterEqual(self.published_post.reading_time, 1)

    def test_get_absolute_url(self):
        expected_url = f'/blog/{self.published_post.slug}/'
        self.assertEqual(self.published_post.get_absolute_url(), expected_url)

    def test_post_queryset_managers(self):
        published = Post.objects.published()
        drafts = Post.objects.drafts()
        featured = Post.objects.featured()

        self.assertIn(self.published_post, published)
        self.assertNotIn(self.draft_post, published)
        self.assertIn(self.draft_post, drafts)
        self.assertIn(self.published_post, featured)

    def test_number_of_likes(self):
        self.assertEqual(self.published_post.number_of_likes(), 0)
        self.published_post.likes.add(self.user)
        self.assertEqual(self.published_post.number_of_likes(), 1)
