import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id, to_global_id
from django.contrib.auth.models import User
from app.models import Profile, Post
from app.types import ProfileNode

from .validations import validate_mutation, validation_dicts
from .auth import Signup
from ..utils import get_user_id


class ProfileCreateData(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()


class ProfileUpdateData(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()


class CreateProfile(relay.ClientIDMutation):
    class Input:
        data = ProfileCreateData()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        return Signup.mutate_and_get_payload(root, info, data)


class UpdateProfile(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        data = ProfileUpdateData()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, username, data):

        validate_mutation(validation_dicts["update_profile"], data)
        qs = Profile.objects.filter(username=username)
        if qs.exists():
            profile = qs.first()
            try:
                obj, _ = Profile.objects.update_or_create(username=username, defaults=data)
                return UpdateProfile(profile=obj)
            except Exception as e:
                raise GraphQLError(f"{e}")
        else:
            raise GraphQLError(f"profile not found")


class DeleteProfile(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, username):
        try:
            obj = Profile.objects.filter(username=username).first()
            if obj is None:
                raise GraphQLError("User not found")
            user = obj.user
            user.delete()
            if obj:
                obj.delete()
            return DeleteProfile(ok=True)
        except Exception as e:
            raise GraphQLError(f"{e}")


class ToggleLike(relay.ClientIDMutation):
    class Input:
        post_id = graphene.ID()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # auth check
        user_id = get_user_id(info)
        if user_id is None:
            raise GraphQLError("You must be logged in to create a post.")

        post_id = kwargs["post_id"]
        user = User.objects.filter(id=user_id).first()
        
        if user is None or user.profile is None:
            raise GraphQLError("User not found")
        else:
            post_ids = user.profile.liked.values_list("id", flat=True)
            if int(post_id) in post_ids:
                user.profile.liked.remove(int(post_id))
            else:
                user.profile.liked.add(int(post_id))
            return ToggleLike(profile=user.profile)
