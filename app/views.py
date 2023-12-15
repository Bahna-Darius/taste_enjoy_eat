from django.shortcuts import render
from app.models import Post, Comments
from app.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    context = {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts
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
