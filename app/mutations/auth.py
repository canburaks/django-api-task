import re
from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id, to_global_id
from app.models import Profile, Post
from app.types import ProfileNode, UserNode
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from .validations import validate_mutation, validation_dicts
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session


class AuthData(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)

class LogoutData(graphene.InputObjectType):
    username = graphene.String(required=False)

class Signup(relay.ClientIDMutation):
    class Input:
        data = AuthData()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        print(data)

        if data is None:
            raise GraphQLError(f"empty data")

        try:
            validate_mutation(validation_dicts["auth"], data)

            username = data["username"]
            if username:
                if User.objects.filter(username=username).exists() is True:
                    raise GraphQLError(f"choose another username")

            password = data["password"]
            regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
            if re.search(regex_password, password) is None:
                raise GraphQLError(
                    f"password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character"
                )

            user = User.objects.create_user(username, password)
            if user:
                qs = Profile.objects.filter(user=user)
                if qs.exists():
                    return Signup(profile=qs.first())
                else:
                    profile = Profile.objects.create(user=user, username=user.username)
                    return Signup(profile=profile)
            else:
                profile = Profile.objects.create(user=user, username=username)
                return profile

        except Exception as e:
            raise GraphQLError(f"{e}")
        raise GraphQLError(f"unknown error")


class Login(relay.ClientIDMutation):
    class Input:
        data = AuthData()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        if data is None:
            raise GraphQLError(f"empty data")
        try:
            username = data["username"]
            if User.objects.filter(username=username).exists() is False:
                raise GraphQLError(f"user not found")
            
            password = data["password"]
            user = authenticate(username=username, password=password)
            print("user", user.is_authenticated, user.username)
            if user.profile:
                return Login(profile=user.profile)
            else:
                profile = Profile.objects.create(user=user, username=username)
                return Login(profile=profile)
        except Exception as e:
            raise GraphQLError(f"Login: {e}")

class Logout(graphene.Mutation):
      
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info):
        if info.context.user.is_authenticated:
            logout(info.context)
            print(info.context.user)
            return LogoutMutation(ok=True)
        else:
            raise GraphQLError(f"user not authenticated")
