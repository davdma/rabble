from factory import Sequence, Faker, SubFactory
from factory.django import DjangoModelFactory
import factory
from rabble.models import User, Community, Subrabble, Post, Comment

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    profile_pic = Faker('image_url')
    short_bio = Faker('sentence')
    interests = Faker('sentence', nb_words=5)

    @factory.post_generation
    def follows(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.follows.add(*extracted)

class CommunityFactory(DjangoModelFactory):
    class Meta:
        model = Community

    community_name = Faker('word')
    owner = SubFactory(UserFactory)

    @factory.post_generation
    def admins(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.admins.add(*extracted)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.members.add(*extracted)

class SubrabbleFactory(DjangoModelFactory):
    class Meta:
        model = Subrabble

    identifier = Faker('word')
    subrabble_name = Faker('word')
    description = Faker('sentence')
    visibility = Faker('random_element', elements=[Subrabble.Visibility.PUBLIC, Subrabble.Visibility.PRIVATE])
    anon_permissions = Faker('boolean')
    community = SubFactory(CommunityFactory)

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    subrabble = SubFactory(SubrabbleFactory)
    title = Faker('sentence')
    body = Faker('paragraph')
    user = SubFactory(UserFactory)
    anon = Faker('boolean')

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
    body = Faker('paragraph')
    anon = Faker('boolean')
    parent = None