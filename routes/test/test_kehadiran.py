from unittest import IsolatedAsyncioTestCase
from sqlalchemy.orm import Session
from main import app
from fastapi.testclient import TestClient
from common.security import generate_hash_password, generate_jwt_token_from_user
from models import factory_session, clear_all_data_on_database
from migrations.factories.UserFactory import UserFactory
from models.Kehadiran import Kehadiran
from repository import kehadiran as kehadiran_repo
import alembic.config

class TestKehadiran(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db : Session = factory_session()
        clear_all_data_on_database(db=self.db)
        return super().setUp()
    
    async def test_paginate_shift(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Hadir",
                keterangan="hadir",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Terlambat",
                keterangan="telat absen",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Lembur",
                keterangan="Lembur kerja",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Izin",
                keterangan="Izin",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Sakit",
                keterangan="sakit",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Bolos",
                keterangan="Kabur kerjaan",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            "/kehadiran",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "count": 6,
            "page_count": 1,
            "page_size": 10,
            "page": 1,
            "results": [
                {
                    "id": val.id,
                    "nama_kehadiran": val.nama_kehadiran,
                    "keterangan": val.keterangan
                }
                for val in data
            ]
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())
    
    async def test_paginate_shift_params(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Hadir",
                keterangan="hadir",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Terlambat",
                keterangan="telat absen",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Lembur",
                keterangan="Lembur kerja",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Izin",
                keterangan="Izin",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Sakit",
                keterangan="sakit",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Bolos",
                keterangan="Kabur kerjaan",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)

        # When
        response = client.get(
            "/kehadiran",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "nama_kehadiran": "aki"
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
                    "id": data[4].id,
                    "nama_kehadiran": data[4].nama_kehadiran,
                    "keterangan": data[4].keterangan
                }
            ]
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())
    
    async def test_detail_kehadiran(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        data = [
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Hadir",
                keterangan="hadir",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Terlambat",
                keterangan="telat absen",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        
        # When
        response = client.get(
            f"/kehadiran/{data[1].id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "id": data[1].id,
            "nama_kehadiran": data[1].nama_kehadiran,
            "keterangan": data[1].keterangan
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())

    async def test_create_kehadiran(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        data = {
            "nama_kehadiran": "Terlambat",
            "keterangan": "telat kerja kesiangan"
        }
        
        # When
        response = client.post(
            "/kehadiran/",
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )
        
        # Expect
        self.assertEqual(response.status_code, 201)
        output = {
            "id": response.json()["id"],
            "nama_kehadiran": data["nama_kehadiran"],
            "keterangan": data["keterangan"]
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())
        check_db = self.db.query(Kehadiran).filter(
            Kehadiran.nama_kehadiran == data["nama_kehadiran"],
            Kehadiran.keterangan == data["keterangan"]
        ).first()
        self.assertIsNotNone(check_db)
    
    
    async def test_update_kehadiran(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        old = [
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Hadir",
                keterangan="hadir",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Terlambat",
                keterangan="telat absen",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        data = {
            "nama_kehadiran": "Terlambat",
            "keterangan": "telat kerja kesiangan"
        }
        
        # When
        response = client.put(
            f"/kehadiran/{old[1].id}",
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )
        
        # Expect
        self.assertEqual(response.status_code, 200)
        output = {
            "id": old[1].id,
            "nama_kehadiran": data["nama_kehadiran"],
            "keterangan": data["keterangan"]
        }
        self.maxDiff = None
        self.assertEqual(output, response.json())
        check_db = self.db.query(Kehadiran).filter(
            Kehadiran.id == old[1].id,
            Kehadiran.nama_kehadiran == data["nama_kehadiran"],
            Kehadiran.keterangan == data["keterangan"]
        ).first()
        self.assertIsNotNone(check_db)

    async def test_delete_kehadiran(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        old = [
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Hadir",
                keterangan="hadir",
                is_commit=False
            ),
            kehadiran_repo.create(
                db=self.db,
                nama_kehadiran="Terlambat",
                keterangan="telat absen",
                is_commit=False
            ),
        ]
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        
        # When
        response = client.delete(
            f"/kehadiran/{old[1].id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        # Expect
        self.assertEqual(response.status_code, 204)
        check_db = self.db.query(Kehadiran).filter(
            Kehadiran.id == old[1].id,
            Kehadiran.nama_kehadiran == old[1].nama_kehadiran,
            Kehadiran.keterangan == old[1].keterangan
        ).first()
        self.assertIsNone(check_db)

    async def test_detail_kehadiran_not_found(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        
        # When
        response = client.get(
            "/kehadiran/091214",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        # Expect
        self.assertEqual(response.status_code, 404)

    async def test_update_kehadiran_not_found(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        
        # When
        response = client.put(
            "/kehadiran/091214",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nama_kehadiran": "ga ada",
                "keterangan": "data ini ga ada"
            }
        )
        
        # Expect
        self.assertEqual(response.status_code, 404)
    
    async def test_delete_kehadiran_not_found(self):
        # Given
        user = UserFactory.create(
            nama="Admin",
            email="admin@example.test",
            password=generate_hash_password("12qwaszx")
        )
        self.db.commit()
        token = await generate_jwt_token_from_user(user)
        client = TestClient(app)
        
        # When
        response = client.delete(
            "/kehadiran/091214",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        # Expect
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()