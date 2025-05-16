from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rabble.models import *
from .serializers import *

@api_view(['GET'])
def subrabble_list(request):
    if request.method == 'GET':
        subrabbles = Subrabble.objects.all()
        serializer = SubrabbleSerializer(subrabbles, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def subrabble_detail(request, identifier):
    try:
        subrabble = Subrabble.objects.get(identifier=identifier)
    except Subrabble.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubrabbleSerializer(subrabble)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def post_list(request, identifier):
    try:
        subrabble = Subrabble.objects.get(identifier=identifier)
    except Subrabble.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        posts = subrabble.post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # make sure that the post is associated with the subrabble
            if 'subrabble' in request.data and request.data['subrabble'] != subrabble.subrabble_name:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer.save(subrabble=subrabble)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, identifier, pk):
    try:
        subrabble = Subrabble.objects.get(identifier=identifier)
        post = subrabble.post_set.get(pk=pk)
    except Subrabble.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNoteExit:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            # do not allow changing the subrabble of a post
            if 'subrabble' in request.data and request.data['subrabble'] != subrabble.subrabble_name:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_like(request, identifier, pk):
    try:
        subrabble = Subrabble.objects.get(identifier=identifier)
        post = subrabble.post_set.get(pk=pk)
    except Subrabble.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.data.get("user")
    if not user:
        return Response({"error": "User field is required."}, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(username=user).count() == 0:
        return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=user)
    if PostLike.objects.filter(post=post, user=user).exists():
        # remove the like
        PostLike.objects.filter(post=post, user=user).delete()
        return Response({"liked": False, "like_count": PostLike.objects.filter(post=post).count()})

    # add the like
    PostLike.objects.create(post=post, user=user)
    return Response({"liked": True, "like_count": PostLike.objects.filter(post=post).count()})