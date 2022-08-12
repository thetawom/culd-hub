import json

import graphene
import graphql_jwt
from django.dispatch import receiver
from graphql_jwt.decorators import login_required, staff_member_required
from graphql_jwt.refresh_token.signals import refresh_token_rotated

from show_manager.models import (
    Member,
    Show,
    SCHOOL_CHOICES,
    CLASS_YEAR_CHOICES,
    MEMBERSHIP_CHOICES,
    SHOW_PRIORITY_CHOICES,
    PERFORMANCE_ROLE_CHOICES,
)
from users.models import User
from .mutations import (
    CreateUserMutation,
    CreateRoleMutation,
    DeleteRoleMutation,
    EditUserMutation,
)
from .types import UserType, MemberType, ShowType


@receiver(refresh_token_rotated)
def revoke_refresh_token(_sender, request, refresh_token, **_kwargs):
    refresh_token.revoke(request)


def tuple_to_json(tuple_dict):
    return json.dumps(dict((k, v) for k, v in tuple_dict))


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    members = graphene.List(MemberType)
    shows = graphene.List(ShowType)
    me = graphene.Field(UserType)

    school_choices = graphene.String()
    class_year_choices = graphene.String()
    membership_choices = graphene.String()
    show_priority_choices = graphene.String()
    performance_role_choices = graphene.String()

    @staticmethod
    @staff_member_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    @staticmethod
    @login_required
    def resolve_members(root, info, **kwargs):
        return Member.objects.all()

    @staticmethod
    def resolve_shows(root, info, **kwargs):
        return Show.objects.filter(is_published=True)

    @staticmethod
    @login_required
    def resolve_me(root, info, **kwargs):
        return User.objects.get(pk=info.context.user.pk)

    @staticmethod
    def resolve_school_choices(root, info, **kwargs):
        return tuple_to_json(SCHOOL_CHOICES)

    @staticmethod
    def resolve_class_year_choices(root, info, **kwargs):
        return tuple_to_json(CLASS_YEAR_CHOICES)

    @staticmethod
    def resolve_membership_choices(root, info, **kwargs):
        return tuple_to_json(MEMBERSHIP_CHOICES)

    @staticmethod
    def resolve_show_priority_choices(root, info, **kwargs):
        return tuple_to_json(SHOW_PRIORITY_CHOICES)

    @staticmethod
    def resolve_performance_role_choices(root, info, **kwargs):
        return tuple_to_json(PERFORMANCE_ROLE_CHOICES)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    create_user = CreateUserMutation.Field()
    create_role = CreateRoleMutation.Field()
    delete_role = DeleteRoleMutation.Field()
    edit_user = EditUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
