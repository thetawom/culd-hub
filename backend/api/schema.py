import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import staff_member_required
from users.models import User
from show_manager.models import Member, Show, Round, Contact

from django.dispatch import receiver
from graphql_jwt.refresh_token.signals import refresh_token_rotated


@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, request, refresh_token, **kwargs):
    refresh_token.revoke(request)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "member")


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = ("user", "membership", "performed_shows", "pointed_shows")


class ShowType(DjangoObjectType):
    class Meta:
        model = Show
        fields = (
            "name",
            "date",
            "time",
            "rounds",
            "address",
            "lions",
            "point",
            "contact",
            "performers",
            "is_campus",
            "priority",
        )


class RoundType(DjangoObjectType):
    class Meta:
        model = Round
        fields = ("show", "time")


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = ("first_name", "last_name", "phone", "email")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    members = graphene.List(MemberType)
    shows = graphene.List(ShowType)

    @staff_member_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_categories(root, info, **kwargs):
        return Member.objects.all()

    def resolve_shows(root, info, **kwargs):
        return Show.objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
