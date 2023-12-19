from django.contrib import admin
from app.models import Post, Tag, Comments, Profile, WebsiteMeta, Subscribe

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
admin.site.register(Subscribe)
