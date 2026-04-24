from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import Genre, Movie, Review
from app.seed import load_seed


def test_load_seed_is_idempotent():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
    )
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    with session_local() as session:
        first_counts = load_seed(session)
        second_counts = load_seed(session)

        assert first_counts["genres"] > 0
        assert first_counts["movies"] > 0
        assert first_counts["reviews"] > 0
        assert second_counts == {
            "genres": 0,
            "directors": 0,
            "actors": 0,
            "movies": 0,
            "reviews": 0,
        }
        assert session.scalar(select(Genre).limit(1)) is not None
        assert session.scalar(select(Movie).limit(1)) is not None
        assert session.scalar(select(Review).limit(1)) is not None

    Base.metadata.drop_all(engine)
    engine.dispose()
