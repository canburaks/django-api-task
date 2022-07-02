import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id
from app.models import Post, Profile
from app.types import PostNode
from .validations import validate_mutation, validation_dicts
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from ..utils import get_user_id
import pprint

pp = pprint.PrettyPrinter(width=41, compact=True)


class CreatePostData(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class UpdatePostData(graphene.InputObjectType):
    id = graphene.ID(required=True)
    title = graphene.String()
    description = graphene.String()


class CreatePost(relay.ClientIDMutation):
    class Input:
        data = CreatePostData()

    post = graphene.Field(PostNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):

        # auth check
        user_id = get_user_id(info)
        if user_id is None:
            raise GraphQLError("You must be logged in to create a post.")
        try:
            validate_mutation(validation_dicts["post"], data)
            user = User.objects.filter(id=user_id).first()
            if user and user.profile:
                post = Post.objects.create(**data, author=user.profile)
                return CreatePost(post=post)
        except Exception as e:
            raise GraphQLError(f"{e}")


class UpdatePost(relay.ClientIDMutation):
    class Input:
        data = UpdatePostData()

    post = graphene.Field(PostNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data):
        # auth check
        user_id = get_user_id(info)
        if user_id is None:
            raise GraphQLError("You must be logged in to create a post.")

        validate_mutation(validation_dicts["post"], data)
        try:
            validate_mutation(validation_dicts["post"], data)
            user = User.objects.filter(id=user_id).first()
            if user and user.profile:
                post = user.profile.posts.filter(id=data["id"])
                if post.exists():
                    post = post.first()
                    post.title = data["title"]
                    post.description = data["description"]
                    post.save()
                    return UpdatePost(post=post)
                else:
                    raise GraphQLError("Post not found")
        except Exception as e:
            raise GraphQLError(f"{e}")


class DeletePost(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # auth check
        user_id = get_user_id(info)
        if user_id is None:
            raise GraphQLError("You must be logged in to create a post.")
        user = User.objects.filter(id=user_id).first()
        if user and user.profile:
            post = user.profile.posts.filter(id=id)
            if post.exists():
                post = post.first()
                post.delete()
                return DeletePost(ok=True)
            else:
                raise GraphQLError("Post not found")
        raise GraphQLError("You must be logged in to create a post.")
