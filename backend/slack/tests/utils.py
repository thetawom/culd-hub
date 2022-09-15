from faker import Faker


def slack_id_faker(faker=None):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    def func(*args, **kwargs):
        return faker.password(length=10, special_chars=False, lower_case=False)

    return func
