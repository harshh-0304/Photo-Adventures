from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db import connection
from blog import constants as CONST
from django.db.models import Count, F, Q
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from taggit.models import Tag


class BlogPosts(generic.ListView,):
    """
    Class view for all blog posts. Returns all posts to blog.html template.
    """
    model = Post
    # Query all published posts - status 2
    queryset = Post.objects.filter(status=2).order_by('-created_on')
    template_name = CONST.BLOG
    paginate_by = CONST.PAGINATION


class SearchPosts(generic.ListView):
    """
    Search published posts by title, content, location, or excerpt.
    """
    model = Post
    template_name = CONST.BLOG
    paginate_by = CONST.PAGINATION

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(location__icontains=query) |
                Q(excerpt__icontains=query),
                status=2
            ).order_by('-created_on')
        return Post.objects.filter(status=2).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class CategoryPosts(generic.ListView):
    """
    Class view to list published posts filtered by category.
    """
    model = Post
    template_name = CONST.BLOG
    paginate_by = CONST.PAGINATION

    def get_queryset(self):
        category = self.kwargs.get('category', '').lower()
        return Post.objects.filter(category=category, status=2).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category', '')
        return context


class AuthorPosts(generic.ListView):
    """
    Class view to list published posts by a specific author username.
    """
    model = Post
    template_name = CONST.BLOG
    paginate_by = CONST.PAGINATION

    def get_queryset(self):
        self.author_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.author_user, status=2).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_user'] = getattr(self, 'author_user', None)
        return context


def api_trending_posts(request):
    """
    JSON API endpoint returning the top 5 trending posts.
    """
    trending = Post.objects.filter(status=2).order_by('-view_count', '-created_on')[:5]
    data = [
        {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'author': post.author.username,
            'category': post.category,
            'view_count': post.view_count,
            'likes_count': post.number_of_likes(),
            'reading_time': post.reading_time,
            'url': post.get_absolute_url(),
        }
        for post in trending
    ]
    return JsonResponse({'status': 'success', 'count': len(data), 'posts': data})






class PostList(generic.ListView):
    """
    Class represents a view that lists all published posts
    and renders it in template "blog.html"
    """
    model = Post
    context_object_name = 'post'
    template_name = CONST.BLOG


def index(request):
    """
    Function represents variables and context to be rendered
    in index.html template.
    """
    # Filter only published posts with more than 0 likes
    trending = Post.objects.filter(status=2, likes__gt=0).annotate(
        like_count=Count('likes')).order_by('-like_count')[:3]

    # Variables to show statistics on the main page
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_likes = Post.objects.aggregate(total_likes=Count('likes')).get(
        'total_likes') or 0
    total_users = User.objects.count()

    return render(request, CONST.INDEX, {
        'trending': trending,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'total_users': total_users,
        })


def about(request):
    """
    Function represents a view that renders about.html page
    """
    return render(request, CONST.ABOUT)


def contact(request):
    """
    Function based view to return user name and user email to the template.
    They are used to prepopulate contact form fields if user is authenticated.
    For anonymous user variables become empty strings to avoid property error.
    Anonymous user does not have email property.
    """
    user_name = request.user.username if request.user.is_authenticated else ""
    user_email = request.user.email if request.user.is_authenticated else ""
    context = {
        'user_name': user_name,
        'user_email': user_email,
    }
    return render(request, CONST.CONTACT, context)


def rules(request):
    """
    Function renders rules.html template
    """
    return render(request, CONST.RULES)


class FullPost(View):
    """
    Class represents a view that renders sigle blog post template
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Method represents a view that displays a single blog post
        It gets published posts with specific slug, comments and likes
        """
        queryset = Post.objects.filter(status=2)  # 2 == published
        post = get_object_or_404(queryset, slug=slug)
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        post.refresh_from_db(fields=['view_count'])
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = post.likes.filter(id=self.request.user.id).exists()

        meta_description = post.excerpt if post.excerpt else post.content[:150]
        meta_image_url = request.build_absolute_uri(post.featured_image.url) if post.featured_image else None
        canonical_url = request.build_absolute_uri(post.get_absolute_url())

        return render(
            request,
            CONST.FULL_POST,
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
                'meta_description': meta_description,
                'meta_image_url': meta_image_url,
                'canonical_url': canonical_url,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Method represents a view that allows users to submit
        comments on single blog post.
        """
        queryset = Post.objects.filter(status=2)  # 2 == published
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        # This checks if current user liked post, filter returns boolean
        liked = post.likes.filter(id=self.request.user.id).exists()
        # Creates a new comment form instance with data from request
        comment_form = CommentForm(data=request.POST)
        # If the form is valid, save the comment and confirm with message
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request, 'Thank you! Your comment is awaiting approval.')
        # If the form is invalid, show form again
        else:
            comment_form = CommentForm()

        # Renders full post template with context variables
        return render(
            request,
            CONST.FULL_POST,
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )


class PostLike(LoginRequiredMixin, View):
    """
    Class based view that allows users to like posts.
    It toggles to add/remove post.likes
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # check if user already liked post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            # display message when like removed
            messages.success(request, 'Like removed!')
        else:
            post.likes.add(request.user)
            # display message when like added
            messages.success(request, 'Like added!')

        return HttpResponseRedirect(reverse('full_post', args=[slug]))


@login_required
def add_post(request):
    """
    Function based view that allows users to add new posts.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(
                request, 'Thank you! Your post was saved.'
                'Check its status in your dashboard')
            return redirect('user_account')
    else:
        form = PostForm()
    return render(request, CONST.ADD_POST, {'form': form})


@login_required
def delete_post(request, slug):
    """
    Function based view that allows users to delete their posts.
    """
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.warning(request, 'Your post was deleted!')
        return redirect('user_account')
    else:
        return render(request, CONST.DELETE_POST, {'post': post})


class PostEdit(View):
    """
    Class based view to allow users to edit posts.
    It uses post model and post form to read and update values.
    """
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)
        form = PostForm(instance=post)
        return render(request, CONST.EDIT_POST, {'form': form})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            content = post.content
            post.save()
            form.save_m2m()
            # display confirmation message
            messages.success(request, 'Changes saved! '
                             'You can check post status in your dashboard.')
            # redirect to user dashboard
            return redirect('user_account')
        else:
            return render(request, CONST.EDIT_POST, {'form': form})


@login_required
def dashboard_stats(request):
    """
    Function represents user dashboard stats and includes
    context variables to render total number of user's published posts,
    total number of drafts and total nubmer of posts awaiting moderation.
    """
    author = request.user
    draft_count = Post.objects.filter(author=author, status=0).count()
    awaiting_moderation_count = Post.objects.filter(
        author=author, status=1).count()
    published_count = Post.objects.filter(author=author, status=2).count()

    context = {
        'published_count': published_count,
        'draft_count': draft_count,
        'awaiting_moderation_count': awaiting_moderation_count,
    }

    return context


@login_required
def user_account(request):
    """
    Function represents user dashboard view and includes
    variables used to display statistics in the template
    """
    user_posts = Post.objects.filter(author=request.user)
    dashboard_stats_data = dashboard_stats(request)
    return render(request, CONST.USER_ACCOUNT,
                  {'user_posts': user_posts,
                   'dashboard_stats': dashboard_stats_data})


class TaggedPosts(generic.ListView):
    """
    Class represents a list of all posts with specific slug.
    It uses Post model and blog.html template to display posts
    in paginated manner.
    """
    model = Post
    template_name = CONST.BLOG
    paginate_by = CONST.PAGINATION

    def get_queryset(self):
        # get tab form the url slug
        tag_slug = self.kwargs['tag_slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        # return posts with tags that are published, order descending
        return Post.objects.filter(tags=tag, status=2).order_by('-created_on')

    def get_context_data(self, **kwargs):
        # add tag to context to be used in the template
        context = super(TaggedPosts, self).get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return context


def robots_txt(request):
    """Serve robots.txt file for search engine web crawlers."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /summernote/",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def health_check(request):
    """System liveness probe verifying database connectivity."""
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
        return JsonResponse({"status": "unhealthy", "database": db_status}, status=503)

    return JsonResponse({
        "status": "healthy",
        "database": db_status,
        "service": "Photo Adventures",
    })

