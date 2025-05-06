from rest_framework import serializers
from rabble.models import *

class SubrabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrabble
        fields = ['id', 'identifier', 'subrabble_name', 'description', 'visibility', 'anon_permissions', 'community']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'subrabble', 'title', 'body', 'user', 'anon']
        read_only_fields = ['subrabble']