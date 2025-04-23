from django.contrib import admin
from rabble.models import User, Community, Subrabble, Post, Comment, PostLike, CommentLike, Conversation, Message
# Register your models here.

admin.site.register(User)
admin.site.register(Community)
admin.site.register(Subrabble)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Conversation)
admin.site.register(Message)
