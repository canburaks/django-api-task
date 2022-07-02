import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from .models import Post, Profile


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        fields = [
            "id",
            "username",
            "profile",
        ]
        filter_fields = ["id", "username"]
    


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node,)
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "user",
            "created_at",
            "updated_at",
            "posts",
            "liked",
        ]
        filter_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "posts",
            "liked",
        ]


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "author",
            "liked_by",
        ]
        filter_fields = [
            "id",
            "created_at",
            "updated_at",
            "author",
            "liked_by",
        ]
