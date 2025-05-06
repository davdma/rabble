from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.TextField(blank=True, null=True)
    short_bio = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    follows = models.ManyToManyField("self", symmetrical=False, blank=True)

class Community(models.Model):
    community_name = models.TextField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='community_admins')
    members = models.ManyToManyField(User, related_name='community_members')

class Subrabble(models.Model):
    class Visibility(models.IntegerChoices):
        PUBLIC = 1, "Public"
        PRIVATE = 2, "Private"
    identifier = models.TextField()
    subrabble_name = models.TextField()
    description = models.TextField(blank=True)
    visibility = models.PositiveSmallIntegerField(choices=Visibility.choices)
    anon_permissions = models.BooleanField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['community_id', 'identifier']

class Post(models.Model):
    subrabble = models.ForeignKey(Subrabble, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anon = models.BooleanField()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    anon = models.BooleanField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name='likes',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Conversation(models.Model):
    title = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    text = models.TextField()

