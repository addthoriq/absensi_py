from models import factory_session
from seeders.users import initial_user
from seeders.roles import initial_role


def initial_seeders():
    with factory_session() as session:
        print("Seeder Role")
        initial_role(db=session, is_commit=False)
        print("Seeder User")
        initial_user(db=session, is_commit=False)
        session.commit()
