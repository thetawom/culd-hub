import graphene
from users.models import User
from .types import UserType


class CreateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String()

    @staticmethod
    def mutate(root, info, first_name, last_name, email, password, phone=""):
        user_instance = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        user_instance.set_password(password)
        user_instance.save()
        return CreateUserMutation(user=user_instance)
