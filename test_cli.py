from unittest import IsolatedAsyncioTestCase
import alembic.config
from models import factory_session, clear_all_data_on_database
from typer.testing import CliRunner
from cli import app
from models.Role import Role
from models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import func

runner = CliRunner()


class TestUserRoleUserSeeder(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "base"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(self.db)
        return super().setUp()

    async def test_initial_data(self) -> None:
        # Given
        result = runner.invoke(app=app, args=["initial-data"])

        # Expect
        print("+++++++++++++++++++++++++++++++")
        print(result.exit_code)
        print("+++++++++++++++++++++++++++++++")
        self.assertEqual(result.exit_code, 0)
        num_role = self.db.query(func.count(Role.id)).scalar()
        num_user = self.db.query(func.count(User.id)).scalar()
        self.assertGreater(num_role, 0)
        self.assertGreater(num_user, 0)

    async def test_initial_migrate(self) -> None:
        # Given
        result = runner.invoke(app=app, args=["initial-migrate"])

        # Expect
        self.assertEqual(result.exit_code, 0)
        num_role = self.db.query(func.count(Role.id)).scalar()
        num_user = self.db.query(func.count(User.id)).scalar()
        self.assertGreater(num_role, 0)
        self.assertGreater(num_user, 0)
        self.db.rollback()

    def tearDown(self) -> None:
        clear_all_data_on_database(self.db)
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
