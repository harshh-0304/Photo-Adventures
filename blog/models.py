from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from blog import constants as CONST
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class PostQuerySet(models.QuerySet):
    """
    Custom QuerySet for Post model providing reusable domain query filters.
    """
    def published(self):
        return self.filter(status=2)

    def drafts(self):
        return self.filter(status=0)

    def trending(self):
        return self.filter(status=2).order_by('-view_count', '-created_on')

    def featured(self):
        return self.filter(status=2, featured=True)


class Post(models.Model):
    """
    Model of the blog post
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='photo_adventures')
    category = models.CharField(choices=CONST.POST_CATEGORIES, max_length=20)
    excerpt = models.TextField(blank=False)
    featured_image = models.ImageField(upload_to='featured_images/', default='placeholder.png')
    location = models.CharField(max_length=100, unique=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=CONST.STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    featured = models.BooleanField(default=False, verbose_name='featured post')
    view_count = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    objects = PostQuerySet.as_manager()

    class Meta:
        """
        Class to set descending order of Posts in Admin Panel
        """
        ordering = ['-created_on']

    def __str__(self):
        """
        Method to return string object
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Auto-generate URL slug from title if not explicitly provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def number_of_likes(self):
        """
        Method to rerunt total number of likes
        """
        return self.likes.count()

    def number_of_comments(self):
        """
        Method to return total number of approved comments
        """
        return self.comments.filter(approved=True).count()

    @property
    def reading_time(self):
        """
        Estimate reading time in minutes based on average 200 words per minute.
        """
        words = len(self.content.split()) if self.content else 0
        return max(1, round(words / 200))

    def get_absolute_url(self):
        """
        Return the canonical URL for a post.
        """
        return reverse('full_post', args=[self.slug])

    @property
    def is_published(self):
        """
        Check if the post has been approved and published.
        """
        return self.status == 2


class TaggedPost(TaggedItemBase):
    """
    Class represents model of post with tags created
    by TaggableManager (taggit)
    """
    content_object = models.ForeignKey('Post', on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Class represents comments that can be added to posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        Class to set ascending order of Comments
        """
        ordering = ['created_on']

    def __str__(self):
        """
        Method to return string
        """
        return f'Comment {self.body} by {self.name}'
