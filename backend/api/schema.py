import graphene
from graphene_django import DjangoObjectType
from users.models import User
from show_manager.models import Member, Show, Round, Contact


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

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_categories(root, info, **kwargs):
        return Member.objects.all()

    def resolve_shows(root, info, **kwargs):
        return Show.objects.all()


schema = graphene.Schema(query=Query)
