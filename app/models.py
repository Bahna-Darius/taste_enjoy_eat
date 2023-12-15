from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    # every time we save a Tags in /Tags_Page/ without id
    # update the slug and return OBJ along with the parameters, and call save()
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    # to return to the Admin Panel, change from Object Class to string
    # string representation
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    view_count = models.IntegerField(null=True, blank=True)


class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # nuull=True / The user can leave a comment even when not logged in.
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='replies')
    # self is used to create a reply to a comment.
    # blank=True / The user can leave a comment even when not logged in.
    # related_name='replies' / to create a reply to a comment.

