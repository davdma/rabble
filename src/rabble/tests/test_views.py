from rabble.tests.factories import UserFactory, CommunityFactory, SubrabbleFactory, PostFactory, CommentFactory
from rabble.models import User, Community, Subrabble, Post, Comment
from django.test import Client
from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_index_view(client):
    community = CommunityFactory.create(community_name="default")
    subrabbles = SubrabbleFactory.create_batch(5, community=community)
    user = UserFactory.create()
    client.force_login(user)
    response = client.get(reverse('index'))

    # Check that all subrabbles listed on the index page
    assert response.status_code == 200
    assert len(response.context['subrabbles']) == 5
    html = response.content.decode()
    for sr in subrabbles:
        assert sr.identifier in html
        assert sr.subrabble_name in html
        assert sr.description in html

@pytest.mark.django_db
def test_subrabble_detail_view(client):
    subrabble = SubrabbleFactory.create()
    posts = PostFactory.create_batch(5, subrabble=subrabble)
    for post in posts:
        CommentFactory.create(post=post)

    # Verifies that the details view for the subRabble has all the posts and numbers of comments
    response = client.get(reverse('subrabble-detail', args=[subrabble.identifier]))

    # Check that all posts listed on the subrabble detail page
    assert response.status_code == 200
    assert len(response.context['posts']) == 5
    for post in response.context['posts']:
        assert post.comments.count() == 1

@pytest.mark.django_db
def test_post_create_view(client):
    subrabble = SubrabbleFactory.create()
    user = UserFactory.create()
    client.force_login(user)
    data = {
        'title': 'Test Post',
        'body': 'This is a test post',
        'anon': False
    }

    response = client.post(reverse('post-create', args=[subrabble.identifier]), data)

    assert response.status_code == 302
    post = Post.objects.latest('id')
    assert post.title == data['title']
    assert post.body == data['body']
    assert post.subrabble == subrabble
    assert post.user == user
