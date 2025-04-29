from rest_framework import serializers
from rabble.models import *

class SubrabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrabble
        fields = ['id', 'identifier', 'subrabble_name', 'description', 'visibility', 'anon_permissions', 'community_id']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'subrabble_id', 'title', 'body', 'user_id', 'anon']
        read_only_fields = ['subrabble_id']