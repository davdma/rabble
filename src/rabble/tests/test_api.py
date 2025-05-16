from rest_framework.test import APIClient
from rabble.tests.factories import SubrabbleFactory, UserFactory, PostFactory
import pytest
from rest_framework import status
from django.urls import reverse
from rabble.models import Post

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_subrabble_get(api_client):
    subrabble = SubrabbleFactory.create()
    response = api_client.get(reverse('subrabble_detail', args=[subrabble.identifier]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['identifier'] == subrabble.identifier
    assert response.data['subrabble_name'] == subrabble.subrabble_name
    assert response.data['description'] == subrabble.description
    assert response.data['visibility'] == subrabble.visibility
    assert response.data['anon_permissions'] == subrabble.anon_permissions

@pytest.mark.django_db
def test_post_post(api_client):
    subrabble = SubrabbleFactory.create()
    user = UserFactory.create()
    data = {
        'subrabble': subrabble.identifier,
        'title': 'Test Post',
        'body': 'This is a test post',
        'anon': False,
        'user': user.username
    }
    response = api_client.post(reverse('post_list', args=[subrabble.identifier]), data)
    assert response.status_code == status.HTTP_201_CREATED

    # confirm that the post was created
    post = Post.objects.get(pk=response.data['id'])
    assert post.subrabble.identifier == subrabble.identifier
    assert post.title == data['title']
    assert post.body == data['body']
    assert post.anon == data['anon']
    assert post.user.username == user.username

@pytest.mark.django_db
def test_post_patch(api_client):
    subrabble = SubrabbleFactory.create()
    post = PostFactory.create(subrabble=subrabble)
    data = {
        'title': 'Updated Post',
        'body': 'This is an updated post',
        'anon': True
    }
    response = api_client.patch(reverse('post_detail', args=[subrabble.identifier, post.id]), data)
    assert response.status_code == status.HTTP_200_OK

    post.refresh_from_db()
    assert post.title == data['title']
    assert post.body == data['body']
    assert post.anon == data['anon']