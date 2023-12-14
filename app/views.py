from django.shortcuts import render
from app.models import Post, Comments
from app.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request, 'app/index.html', context)


def post_page(request, slug):
    # To update the URL based on the title blog.
    posts = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comments.objects.filter(post=posts)

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
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
