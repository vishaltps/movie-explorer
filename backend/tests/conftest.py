"""Shared pytest fixtures: in-memory SQLite engine, sample catalog, FastAPI TestClient."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Actor, Director, Genre, Movie, Review


@pytest.fixture
def engine():
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture
def db(engine) -> Generator[Session, None, None]:
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def db_session(db: Session) -> Session:
    return db


@pytest.fixture
def sample_catalog(db: Session) -> dict[str, object]:
    drama = Genre(id=1, name="Drama", slug="drama")
    history = Genre(id=2, name="History", slug="history")
    sci_fi = Genre(id=3, name="Sci-Fi", slug="sci-fi")

    nolan = Director(
        id=1,
        name="Christopher Nolan",
        birth_year=1970,
        bio="British-American director.",
    )
    villeneuve = Director(
        id=2,
        name="Denis Villeneuve",
        birth_year=1967,
        bio="French Canadian director.",
    )

    cillian = Actor(id=1, name="Cillian Murphy", birth_year=1976, bio="Irish actor.")
    emily = Actor(id=2, name="Emily Blunt", birth_year=1983, bio="British actress.")
    amy = Actor(id=3, name="Amy Adams", birth_year=1974, bio="American actress.")

    oppenheimer = Movie(
        id=1,
        title="Oppenheimer",
        release_year=2023,
        synopsis="The story of J. Robert Oppenheimer.",
        runtime_minutes=180,
        director=nolan,
        average_rating=4.5,
        genres=[drama, history],
        actors=[cillian, emily],
    )
    arrival = Movie(
        id=2,
        title="Arrival",
        release_year=2016,
        synopsis="A linguist communicates with alien visitors.",
        runtime_minutes=116,
        director=villeneuve,
        average_rating=5.0,
        genres=[drama, sci_fi],
        actors=[amy],
    )

    review_1 = Review(
        id=1,
        movie=oppenheimer,
        author_name="alice",
        rating=5,
        comment="Brilliant historical epic.",
    )
    review_2 = Review(
        id=2,
        movie=arrival,
        author_name="bob",
        rating=5,
        comment="Thoughtful and moving science fiction.",
    )

    db.add_all(
        [
            drama,
            history,
            sci_fi,
            nolan,
            villeneuve,
            cillian,
            emily,
            amy,
            oppenheimer,
            arrival,
            review_1,
            review_2,
        ]
    )
    db.commit()

    return {
        "genres": [drama, history, sci_fi],
        "directors": [nolan, villeneuve],
        "actors": [cillian, emily, amy],
        "movies": [oppenheimer, arrival],
        "reviews": [review_1, review_2],
    }


@pytest.fixture
def client(db: Session, sample_catalog: dict[str, object]) -> Generator[TestClient, None, None]:
    del sample_catalog

    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
