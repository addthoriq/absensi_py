import factory
from models import factory_session
from models.Role import Role


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = factory_session

    jabatan = factory.Faker("name")
