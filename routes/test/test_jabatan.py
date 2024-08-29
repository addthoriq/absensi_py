from unittest import IsolatedAsyncioTestCase
from sqlalchemy.orm import Session
from models.Role import Role
from fastapi.testclient import TestClient
from main import app
from common.security import generate_jwt_token_from_user, generate_hash_password
import alembic.config
from models import factory_session, clear_all_data_on_database
from migrations.factories.RoleFactory import RoleFactory
from migrations.factories.UserFactory import UserFactory


class TestJabatan(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(self.db)
        return super().setUp()

    async def test_paginate_jabatan(self):
        # Given
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            "/jabatan", 
            headers={"Authorization": f"Bearer {token}"}
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "count": 3,
            "page_count": 1,
            "page_size": 10,
            "page": 1,
            "results": [
                {
                    "id": val.id,
                    "nama_jabatan": val.jabatan,
                }
                for val in list_role
            ],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_paginate_nama_params(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        user = UserFactory.create(
            email="operator@example.com",
            nama="operator",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[1],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            "/jabatan",
            headers={"Authorization": f"Bearer {token}"},
            params={"nama_jabatan": "dmi"},
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "count": 1,
            "page_count": 1,
            "page_size": 10,
            "page": 1,
            "results": [
                {
                    "id": list_role[0].id,
                    "nama_jabatan": list_role[0].jabatan,
                }
            ],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_detail_jabatan(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        user = UserFactory.create(
            email="guru@example.com",
            nama="Guru",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[2],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            f"/jabatan/{list_role[0].id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "id": list_role[0].id,
            "nama_jabatan": list_role[0].jabatan,
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_detail_jabatan_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            "/jabatan/2001",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    async def test_create_jabatan(self):
        # Given
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        admin = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(admin)
        client = TestClient(app)
        user_request = {
            "nama_jabatan": "Karyawan",
        }

        # When
        response = client.post(
            "/jabatan",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 201)
        output = {
            "id": response.json()["id"],
            "nama_jabatan": user_request["nama_jabatan"],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)
        check_db = (
            self.db.query(Role)
            .filter(
                Role.jabatan == user_request["nama_jabatan"],
            )
            .first()
        )
        self.assertIsNotNone(check_db)

    async def test_update_jabatan(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Gruw"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        user_request = {
            "nama_jabatan": "Guru",
        }

        # When
        response = client.put(
            f"/jabatan/{list_role[1].id}",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        check_db = (
            self.db.query(Role)
            .filter(
                Role.jabatan == user_request["nama_jabatan"],
            )
            .first()
        )
        self.assertIsNotNone(check_db)

    async def test_update_jabatan_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        user_request = {
            "nama_jabatan": "Guru"
        }

        # When
        response = client.put(
            "/jabatan/2001",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    async def test_delete_jabatan(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Guru"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.delete(
            f"/jabatan/{list_role[1].id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 204)
        check_db = self.db.query(Role).filter(Role.id == list_role[1].id).first()
        self.assertIsNone(check_db)

    async def test_delete_jabatan_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        user = UserFactory.create(
            email="admin@example.com",
            nama="Admin",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[0],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.delete(
            "/jabatan/2001",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
