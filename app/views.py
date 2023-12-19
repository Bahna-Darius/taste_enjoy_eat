from django.shortcuts import render
from app.models import Post, Comments, Tag, Profile, WebsiteMeta
from app.forms import CommentForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm(request.POST)
    subscribe_successful = None  # To display a message if the user subscribes successfully.
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            if not request.session.get('subscribe_successful', False):
                subscribe_form.save()
                request.session['subscribe_successful'] = True
                subscribe_successful = 'Thank you for subscribing!'
                subscribe_form = SubscribeForm()

    context = {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'subscribe_form': subscribe_form,
        'subscribe_successful': subscribe_successful,
        'featured_blog': featured_blog,
        'website_info': website_info
    }

    return render(request, 'app/index.html', context)


def post_page(request, slug):
    # To update the URL based on the title blog.
    posts = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=posts, parent=None)
    # this form to add comments and replies.
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent_obj = None
            # If the comment is a reply to another comment.
            # The parent is the id of the comment being replied to.
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_replay = comment_form.save(commit=False)
                    comment_replay.parent = parent_obj
                    comment_replay.post = posts
                    comment_replay.save()
                    return HttpResponseRedirect(reverse(viewname='post_page', kwargs={'slug': slug}
                                                        ))
            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse(viewname='post_page', kwargs={'slug': slug}
                                                    ))

    if posts.view_count is None:
        posts.view_count = 1

    # Increment the view_count each time a blog title is accessed.
    else:
        posts.view_count = posts.view_count + 1
    posts.save()

    context = {
        'post': posts,
        'form': form,
        'comments': comments
    }

    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tags = Tag.objects.all()
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__post__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__post__in=[tag.id]).order_by('-last_updated')[0:2]

    context = {
        'tag': tag,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'tags': tags
    }

    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')

    context = {
        'profile': profile,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors': top_authors
    }

    return render(request, 'app/author.html', context)


def search_post(request):
    search_query = ''   # To display the search query in the search results page.

    if request.GET.get('q'):    # q is the name of the input field in the search form.
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)

    context = {
        'posts': posts,
        'search_query': search_query
    }

    return render(request, 'app/search.html', context)


def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
        'website_info': website_info
    }

    return render(request, 'app/about.html', context)
