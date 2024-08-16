from unittest import IsolatedAsyncioTestCase
import alembic.config
from sqlalchemy.orm import Session
from models import factory_session, clear_all_data_on_database
from common.security import (
    generate_hash_password,
    validated_user_password,
    generate_jwt_token_from_user,
    get_user_from_jwt_token,
)
from migrations.factories.UserFactory import UserFactory


class TestSecurity(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(db=self.db)
        return super().setUp()

    async def test_hash_password(self):
        # Given
        password = "abc123!"
        hash = generate_hash_password(password=password)
        # When
        result = validated_user_password(hash=hash, password=password)
        # Expect
        self.assertTrue(result)

    async def test_jwt_token(self):
        # Given
        user = UserFactory.create(
            email="test@example.com", nama="test", password="12qwaszx"
        )
        self.db.commit()

        # When
        token = await generate_jwt_token_from_user(user)
        token_user = get_user_from_jwt_token(db=self.db, jwt_token=token)

        # Expect
        self.assertIsNotNone(token_user)
        self.assertEqual(user.id, token_user.id)
        self.assertEqual(user.email, token_user.email)
        self.assertEqual(user.nama, token_user.nama)

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
