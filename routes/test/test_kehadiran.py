from unittest import IsolatedAsyncioTestCase
from sqlalchemy.orm import Session
from main import app
from fastapi.testclient import TestClient
from common.security import generate_hash_password, generate_jwt_token_from_user
from models import factory_session, clear_all_data_on_database
from migrations.factories.UserFactory import UserFactory
from models.Kehadiran import Kehadiran
from repository.kehadiran import Kehadiran as kehadiran_repo
import alembic.config

class TestKehadiran(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        self.db : Session = factory_session()
        clear_all_data_on_database(db=self.db)
        return super().setUp()
    
    def tearDown(self) -> None:
        self.db.rollback()
        factory_session.remove()
        return super().tearDown()