import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_session
from app.main import app
from app.models import Base


@pytest.fixture(name="session")
def session_fixture():
    # StaticPool garante que todas as conexões do engine compartilham o mesmo
    # banco em memória — sem ele, cada conexão abre um banco novo e vazio,
    # então as tabelas criadas pelo create_all ficam invisíveis para a sessão
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
