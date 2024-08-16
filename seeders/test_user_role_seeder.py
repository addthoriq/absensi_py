from unittest import IsolatedAsyncioTestCase
import alembic.config
from models import factory_session, clear_all_data_on_database
from models.Role import Role
from models.User import User
from seeders.roles import initial_role
from seeders.users import initial_user
from sqlalchemy.orm import Session
from sqlalchemy import select


class TestUserRoleUserSeeder(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "base"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(self.db)
        return super().setUp()

    async def test_role_seeder(self):
        # Given
        initial_role(db=self.db)

        # When
        check_db = self.db.execute(select(Role)).scalars().all()

        # Expect
        self.assertIsNotNone(check_db)

    async def test_user_seeder(self):
        # Given
        initial_role(db=self.db)
        initial_user(db=self.db)

        # When
        check_db = self.db.query(User).filter(User.email == "admin@absensi.py").first()

        # Expect
        self.assertIsNotNone(check_db)
        self.assertIsNotNone(check_db.role_id)

    def tearDown(self) -> None:
        clear_all_data_on_database(self.db)
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
