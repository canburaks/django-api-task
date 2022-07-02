from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.post import CreatePost, DeletePost, UpdatePost
from .mutations.profile import CreateProfile, DeleteProfile, UpdateProfile, ToggleLike
from .mutations.auth import Login, Signup, Logout
from .types import PostNode, ProfileNode
from .models import Post, Profile


class Query(ObjectType):
    post = relay.Node.Field(PostNode)
    posts = DjangoFilterConnectionField(PostNode)

    profile = relay.Node.Field(ProfileNode)
    profiles = DjangoFilterConnectionField(ProfileNode)

    def resolve_all_posts(root, info, **kwargs):
        print("root-info", root, info.context)
        print(kwargs)
        return Post.objects.all().select_related("author")[: kwargs["first"]]


class Mutation(ObjectType):
    create_profile = CreateProfile.Field()
    create_post = CreatePost.Field()

    update_profile = UpdateProfile.Field()
    update_post = UpdatePost.Field()

    delete_profile = DeleteProfile.Field()
    delete_post = DeletePost.Field()

    toggle_like = ToggleLike.Field()
    
    login = Login.Field()
    signup = Signup.Field()
    logout = Logout.Field()
