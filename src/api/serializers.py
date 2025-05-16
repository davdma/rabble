from rest_framework import serializers
from rabble.models import *

class SubrabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrabble
        fields = ['id', 'identifier', 'subrabble_name', 'description', 'visibility', 'anon_permissions', 'community']

class PostSerializer(serializers.ModelSerializer):
    subrabble = serializers.SlugRelatedField(queryset=Subrabble.objects.all(), slug_field='identifier')
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = Post
        fields = ['id', 'subrabble', 'title', 'body', 'user', 'anon']
        read_only_fields = ['subrabble']