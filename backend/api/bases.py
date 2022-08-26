import graphene

from api.types import ExpectedErrorType
from users.exceptions import WrongUsage


class Output:
    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(ExpectedErrorType)


class DynamicArgsMixin:
    _meta = None
    _args = {}
    _required_args = {}

    @classmethod
    def Field(cls, *args, **kwargs):
        if isinstance(cls._args, dict):
            for key in cls._args:
                cls._meta.arguments.update(
                    {key: graphene.Argument(getattr(graphene, cls._args[key]))}
                )
        elif isinstance(cls._args, list):
            for key in cls._args:
                cls._meta.arguments.update({key: graphene.String()})

        if isinstance(cls._required_args, dict):
            for key in cls._required_args:
                cls._meta.arguments.update(
                    {
                        key: graphene.Argument(
                            getattr(graphene, cls._required_args[key]), required=True
                        )
                    }
                )
        elif isinstance(cls._required_args, list):
            for key in cls._required_args:
                cls._meta.arguments.update({key: graphene.String(required=True)})

        super_Field = getattr(super(), "Field")
        if not super_Field or not callable(super_Field):
            raise WrongUsage("DynamicArgsMixin must have graphene.Mutation as parent")
        return super_Field(*args, **kwargs)
