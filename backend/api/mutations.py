import graphene
from graphql_jwt.decorators import login_required

from show_manager.models import Show, Member, Role
from users.mixins import (
    SendPasswordResetEmailMixin,
    LogoutUserMixin,
    ResetPasswordMixin,
    RegisterMixin,
)
from users.models import User
from .bases import DynamicArgsMixin
from .types import RoleType, UserType


class RegisterMutation(DynamicArgsMixin, RegisterMixin, graphene.Mutation):
    __doc__ = RegisterMixin.__doc__
    _required_args = ["email", "password1", "password2", "first_name", "last_name"]
    _args = ["phone"]


class CreateRoleMutation(graphene.Mutation):
    role = graphene.Field(RoleType)

    class Arguments:
        show_id = graphene.ID(required=True)

    @staticmethod
    def mutate(root, info, show_id):
        role_instance = Role(
            show=Show.objects.get(pk=show_id),
            performer=Member.objects.get(pk=info.context.user.member.id),
        )
        role_instance.save()
        return CreateRoleMutation(role=role_instance)


class DeleteRoleMutation(graphene.Mutation):
    role = graphene.Field(RoleType)

    class Arguments:
        show_id = graphene.ID(required=True)

    @staticmethod
    def mutate(root, info, show_id):
        role_instance = Role.objects.get(
            show=Show.objects.get(pk=show_id),
            performer=Member.objects.get(pk=info.context.user.member.id),
        )
        role_instance.delete()
        return DeleteRoleMutation(role=role_instance)


class EditUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        school = graphene.String()
        class_year = graphene.String()

    @staticmethod
    @login_required
    def mutate(root, info, **kwargs):
        user_instance = User.objects.get(pk=info.context.user.pk)
        for key, value in kwargs.items():
            if hasattr(user_instance, key):
                setattr(user_instance, key, value)
            elif hasattr(user_instance.member, key):
                setattr(user_instance.member, key, value)
        user_instance.save()
        user_instance.member.save()
        return EditUserMutation(user=user_instance)


class LogoutUserMutation(LogoutUserMixin, graphene.Mutation):
    __doc__ = LogoutUserMixin.__doc__


class SendPasswordResetEmailMutation(
    DynamicArgsMixin, SendPasswordResetEmailMixin, graphene.Mutation
):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_args = {"email": "String"}


class ResetPasswordMutation(DynamicArgsMixin, ResetPasswordMixin, graphene.Mutation):
    __doc__ = ResetPasswordMixin.__doc__
    _required_args = {"user_id": "ID", "token": "String", "password": "String"}
