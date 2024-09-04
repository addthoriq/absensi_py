from unittest import IsolatedAsyncioTestCase
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from common.security import generate_jwt_token_from_user, generate_hash_password
import alembic.config
from models import factory_session, clear_all_data_on_database
from migrations.factories.UserFactory import UserFactory
from repository import shift as shift_repo

class TestShift(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db : Session = factory_session()
        clear_all_data_on_database(db=self.db)
        return super().setUp()
    
    async def test_paginate(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.com",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Pagi",
                jam_mulai="07:00:00",
                jam_akhir="12:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Siang",
                jam_mulai="13:00:00",
                jam_akhir="18:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Sore",
                jam_mulai="19:00:00",
                jam_akhir="00:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Malam",
                jam_mulai="01:00:00",
                jam_akhir="06:00:00",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user=user)
        client = TestClient(app)
        
        # When
        response = client.get(
            "/shift",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "count": 4,
            "page_count": 1,
            "page_size": 10,
            "page": 1,
            "results": [
                {
                    "id": val.id,
                    "nama_shift": val.nama_shift,
                    "jam_mulai": str(val.jam_mulai),
                    "jam_akhir": str(val.jam_akhir)
                }
                for val in data
            ] 
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())

    async def test_paginate_params_nama(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.com",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Pagi",
                jam_mulai="07:00:00",
                jam_akhir="12:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Siang",
                jam_mulai="13:00:00",
                jam_akhir="18:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Sore",
                jam_mulai="19:00:00",
                jam_akhir="00:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Malam",
                jam_mulai="01:00:00",
                jam_akhir="06:00:00",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user=user)
        client = TestClient(app)
        
        # When
        response = client.get(
            "/shift",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "nama_shift": "ore"
            }
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
                    "id": data[2].id,
                    "nama_shift": data[2].nama_shift,
                    "jam_mulai": str(data[2].jam_mulai),
                    "jam_akhir": str(data[2].jam_akhir)
                }
            ] 
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())
    
    async def test_paginate_params_jam(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.com",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Pagi",
                jam_mulai="07:00:00",
                jam_akhir="12:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Siang",
                jam_mulai="13:00:00",
                jam_akhir="18:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Sore",
                jam_mulai="19:00:00",
                jam_akhir="00:00:00",
                is_commit=False
            ),
            shift_repo.create(
                db=self.db,
                nama_shift="Shift Malam",
                jam_mulai="01:00:00",
                jam_akhir="06:00:00",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user=user)
        client = TestClient(app)
        
        # When
        response = client.get(
            "/shift",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "jam_mulai": "01:00:00",
                "jam_akhir": "12:00:00"
            }
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
                    "id": data[x].id,
                    "nama_shift": data[x].nama_shift,
                    "jam_mulai": str(data[x].jam_mulai),
                    "jam_akhir": str(data[x].jam_akhir)
                }
                for x in [0,2,3]
            ] 
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()