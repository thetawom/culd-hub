import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required, staff_member_required
from users.models import User
from show_manager.models import Member, Show
from .types import UserType, MemberType, ShowType

from django.dispatch import receiver
from graphql_jwt.refresh_token.signals import refresh_token_rotated


@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, request, refresh_token, **kwargs):
    refresh_token.revoke(request)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    members = graphene.List(MemberType)
    shows = graphene.List(ShowType)

    @staff_member_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_members(root, info, **kwargs):
        return Member.objects.all()

    @login_required
    def resolve_shows(root, info, **kwargs):
        return Show.objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
