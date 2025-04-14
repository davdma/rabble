from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.TextField(blank=True, null=True)
    short_bio = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    follows = models.ManyToManyField("self", symmetrical=False)

class Community(models.Model):
    community_name = models.TextField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='community_admins')
    members = models.ManyToManyField(User, related_name='community_members')

class Subrabble(models.Model):
    class Visibility(models.IntegerChoices):
        PUBLIC = 1, "Public"
        PRIVATE = 2, "Private"
    subrabble_name = models.TextField()
    description = models.TextField()
    visibility = models.PositiveSmallIntegerField(choices=Visibility.choices)
    anon_permissions = models.BooleanField()
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['community_id', 'subrabble_name']

class Post(models.Model):
    subrabble_id = models.ForeignKey(Subrabble, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    anon = models.BooleanField()

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    anon = models.BooleanField()
    parent_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

class Likes(models.Model):
    class Likeable(models.IntegerChoices):
        COMMENT = 1, "Comment"
        POST = 2, "Post"
    comment_id = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    likeable_type = models.PositiveSmallIntegerField(choices=Likeable.choices)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Conversation(models.Model):
    title = models.TextField()
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    text = models.TextField()

