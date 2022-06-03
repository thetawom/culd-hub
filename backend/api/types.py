from graphene_django import DjangoObjectType
from users.models import User
from show_manager.models import Member, Show, Round, Contact, Role


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "member")


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = (
            "id",
            "user",
            "membership",
            "school",
            "class_year",
            "performed_shows",
            "pointed_shows",
        )


class ShowType(DjangoObjectType):
    class Meta:
        model = Show
        fields = (
            "id",
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
            "is_open",
        )


class RoundType(DjangoObjectType):
    class Meta:
        model = Round
        fields = ("id", "show", "time")


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "phone", "email")


class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = ("id", "show", "performer", "role")
