from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post


class ViewIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewtester',
            password='securepassword123'
        )
        self.post = Post.objects.create(
            title='Alpine Peaks Adventure',
            slug='alpine-peaks-adventure',
            author=self.user,
            category='landscape',
            excerpt='Hiking through snow-capped summits.',
            content='Full alpine trek report and pictures.',
            status=2,
            location='Innsbruck'
        )

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Photo Adventures')

    def test_health_check_endpoint(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'healthy')

    def test_robots_txt_endpoint(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User-agent: *', response.content.decode('utf-8'))

    def test_blog_posts_view(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alpine Peaks Adventure')

    def test_search_posts_view(self):
        response = self.client.get(reverse('search_posts') + '?q=Alpine')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alpine Peaks Adventure')

    def test_category_posts_view(self):
        response = self.client.get(reverse('category_posts', args=['landscape']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alpine Peaks Adventure')

    def test_trending_posts_api(self):
        response = self.client.get(reverse('api_trending_posts'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertGreaterEqual(data.get('count'), 1)

    def test_full_post_view_and_view_count_increment(self):
        initial_views = self.post.view_count
        response = self.client.get(reverse('full_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alpine Peaks Adventure')

        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, initial_views + 1)
