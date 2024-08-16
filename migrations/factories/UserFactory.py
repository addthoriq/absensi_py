import factory
from faker import Faker
from common.security import generate_hash_password
from models import factory_session
from models.User import User


def generate_password() -> str:
    fake = Faker()
    return generate_hash_password(fake.password())


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = factory_session

    email = factory.Faker("email")
    nama = factory.Faker("name")
    password = factory.LazyFunction(generate_password)

    @factory.post_generation
    def userRole(self, userRole, extracted, **kwargs):
        if not userRole:
            return
        if extracted:
            self.userRole = extracted
