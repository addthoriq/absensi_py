from unittest import IsolatedAsyncioTestCase
import alembic.config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from common.security import (
    generate_jwt_token_from_user,
    generate_hash_password,
)
from models import factory_session, clear_all_data_on_database
from migrations.factories.UserFactory import UserFactory
from migrations.factories.RoleFactory import RoleFactory
from main import app


class TestAuth(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(self.db)
        return super().setUp()

    async def test_login(self) -> None:
        # Given
        _ = UserFactory.create(
            email="test@example.com",
            nama="test",
            password=generate_hash_password("12qwaszx"),
        )
        self.db.commit()
        client = TestClient(app)

        # When
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "12qwaszx"},
        )

        # Expect
        self.assertEqual(response.status_code, 200)

    async def test_me(self) -> None:
        # Given
        role = RoleFactory.create(jabatan="Admin")
        user = UserFactory.create(
            email="test@example.com",
            nama="test",
            password=generate_hash_password("12qwaszx"),
            userRole=role,
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "id": user.id,
            "nama": user.nama,
            "email": user.email,
            "jabatan": {"id": role.id, "nama_jabatan": role.jabatan},
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
