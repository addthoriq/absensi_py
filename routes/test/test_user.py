from unittest import IsolatedAsyncioTestCase
from sqlalchemy.orm import Session
from models.User import User
from fastapi.testclient import TestClient
from main import app
from common.security import generate_jwt_token_from_user, generate_hash_password
import alembic.config
from models import factory_session, clear_all_data_on_database
from migrations.factories.UserFactory import UserFactory
from migrations.factories.RoleFactory import RoleFactory


class TestUser(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db: Session = factory_session()
        clear_all_data_on_database(self.db)
        return super().setUp()

    async def test_paginate_user(self):
        # Given
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="operator@example.com",
                nama="operator",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[1],
            ),
            UserFactory.create(
                email="guru@example.com",
                nama="Guru",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[2],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            "/user-management", headers={"Authorization": f"Bearer {token}"}
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
                    "nama_user": val.nama,
                    "email": val.email,
                    "jabatan": {
                        "id": val.userRole.id,
                        "nama_jabatan": val.userRole.jabatan,
                    }
                    if val.userRole
                    else None,
                }
                for val in list_users
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
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="operator@example.com",
                nama="operator",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[1],
            ),
        ]
        data = UserFactory.create(
            email="guru@example.com",
            nama="Guru",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[2],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            "/user-management",
            headers={"Authorization": f"Bearer {token}"},
            params={"nama_user": "uru"},
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
                    "id": data.id,
                    "nama_user": data.nama,
                    "email": data.email,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    }
                    if data.userRole
                    else None,
                }
            ],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_paginate_email_params(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="operator@example.com",
                nama="operator",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[1],
            ),
        ]
        data = UserFactory.create(
            email="guru@example.com",
            nama="Guru",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[2],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            "/user-management",
            headers={"Authorization": f"Bearer {token}"},
            params={"email": "uru@exam"},
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
                    "id": data.id,
                    "nama_user": data.nama,
                    "email": data.email,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    }
                    if data.userRole
                    else None,
                }
            ],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_paginate_jabatan_params(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="operator@example.com",
                nama="operator",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[1],
            ),
        ]
        data = UserFactory.create(
            email="guru@example.com",
            nama="Guru",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[2],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            "/user-management",
            headers={"Authorization": f"Bearer {token}"},
            params={"jabatan": list_role[2].id},
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
                    "id": data.id,
                    "nama_user": data.nama,
                    "email": data.email,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    }
                    if data.userRole
                    else None,
                }
            ],
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_detail_user(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
            RoleFactory.create(jabatan="Operator"),
            RoleFactory.create(jabatan="Guru"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="operator@example.com",
                nama="operator",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[1],
            ),
        ]
        data = UserFactory.create(
            email="guru@example.com",
            nama="Guru",
            password=generate_hash_password("12qwaszx"),
            userRole=list_role[2],
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            f"/user-management/{data.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "id": data.id,
            "nama_user": data.nama,
            "email": data.email,
            "jabatan": {"id": data.userRole.id, "nama_jabatan": data.userRole.jabatan}
            if data.userRole
            else None,
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)

    async def test_detail_user_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.get(
            "/user-management/2001",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    async def test_create_user(self):
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
            "email": "user@email.com",
            "nama_user": "User Test",
            "password": "12qwaszx",
            "jabatan": list_role[2].id,
        }

        # When
        response = client.post(
            "/user-management",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 201)
        output = {
            "id": response.json()["id"],
            "nama_user": user_request["nama_user"],
            "email": user_request["email"],
            "jabatan": {"id": list_role[2].id, "nama_jabatan": list_role[2].jabatan},
        }
        self.maxDiff = None
        self.assertEqual(response.json(), output)
        check_db = (
            self.db.query(User)
            .filter(
                User.nama == user_request["nama_user"],
                User.email == user_request["email"],
            )
            .first()
        )
        self.assertIsNotNone(check_db)

    async def test_update_user(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
            UserFactory.create(
                email="guru@example.com",
                nama="Guru",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)
        user_request = {
            "email": "user@email.com",
            "nama_user": "User Test",
            "jabatan": list_role[0].id,
        }

        # When
        response = client.put(
            f"/user-management/{list_users[1].id}",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        check_db = (
            self.db.query(User)
            .filter(
                User.email == user_request["email"],
                User.nama == user_request["nama_user"],
            )
            .first()
        )
        self.assertIsNotNone(check_db)

    async def test_update_user_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)
        user_request = {
            "email": "user@email.com",
            "nama_user": "User Test",
            "jabatan": list_role[0].id,
        }

        # When
        response = client.put(
            "/user-management/2001",
            headers={"Authorization": f"Bearer {token}"},
            json=user_request,
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    async def test_delete_user(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.delete(
            f"/user-management/{list_users[0].id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 204)
        check_db = self.db.query(User).filter(User.id == list_users[0].id).first()
        self.assertIsNone(check_db)

    async def test_delete_user_not_found(self):
        list_role = [
            RoleFactory.create(jabatan="Admin"),
        ]
        list_users = [
            UserFactory.create(
                email="admin@example.com",
                nama="Admin",
                password=generate_hash_password("12qwaszx"),
                userRole=list_role[0],
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(list_users[0])
        client = TestClient(app)

        # When
        response = client.delete(
            "/user-management/2001",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Expect
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()
