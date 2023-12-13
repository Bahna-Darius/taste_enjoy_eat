from django.shortcuts import render
from app.models import Post
from app.forms import CommentForm


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request, 'app/index.html', context)


def post_page(request, slug):
    # To update the URL based on the title blog.
    posts = Post.objects.get(slug=slug)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            postid = request.POST.get('post_id')
            post = Post.objects.get(id=postid)
            comment.post = post
            comment.save()

    if posts.view_count is None:
        posts.view_count = 1

    # Increment the view_count each time a blog title is accessed.
    else:
        posts.view_count = posts.view_count + 1
    posts.save()

    context = {
        'post': posts,
        'form': form
    }

    return render(request, 'app/post.html', context)
