import graphene
import graphql_jwt
from django.dispatch import receiver
from graphql_jwt.decorators import login_required, staff_member_required
from graphql_jwt.refresh_token.signals import refresh_token_rotated

from show_manager.models import Member, Show
from users.models import User
from .mutations import CreateUserMutation, CreateRoleMutation, DeleteRoleMutation
from .types import UserType, MemberType, ShowType


@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, request, refresh_token, **kwargs):
    refresh_token.revoke(request)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    members = graphene.List(MemberType)
    shows = graphene.List(ShowType)
    me = graphene.Field(UserType)

    @staff_member_required
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_members(self, info, **kwargs):
        return Member.objects.all()

    @login_required
    def resolve_shows(self, info, **kwargs):
        return Show.objects.filter(is_published=True)

    @login_required
    def resolve_me(self, info, **kwargs):
        return User.objects.get(pk=info.context.user.pk)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    create_user = CreateUserMutation.Field()
    create_role = CreateRoleMutation.Field()
    delete_role = DeleteRoleMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
