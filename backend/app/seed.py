"""Seed loader — populates the DB with minimal data. Full curated dataset added in a later commit."""
from sqlalchemy import select

from app.db import Base, SessionLocal, engine
from app.models import Actor, Director, Genre, Movie, Review


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.scalar(select(Genre.id).limit(1)) is not None:
            return

        drama = Genre(name="Drama", slug="drama")
        sci_fi = Genre(name="Sci-Fi", slug="sci-fi")
        nolan = Director(name="Christopher Nolan", birth_year=1970)
        villeneuve = Director(name="Denis Villeneuve", birth_year=1967)
        actors = [
            Actor(name="Timothée Chalamet", birth_year=1995),
            Actor(name="Zendaya", birth_year=1996),
            Actor(name="Cillian Murphy", birth_year=1976),
        ]
        db.add_all([drama, sci_fi, nolan, villeneuve, *actors])
        db.flush()

        dune = Movie(
            title="Dune",
            release_year=2021,
            average_rating=8.0,
            genres=[sci_fi],
            director=villeneuve,
            actors=[actors[0], actors[1]],
            synopsis="A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
            runtime_minutes=155,
        )
        oppenheimer = Movie(
            title="Oppenheimer",
            release_year=2023,
            average_rating=8.4,
            genres=[drama],
            director=nolan,
            actors=[actors[2]],
            synopsis="The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
            runtime_minutes=180,
        )
        db.add_all([dune, oppenheimer])
        db.flush()

        db.add_all([
            Review(movie_id=dune.id, author_name="alice", rating=4, comment="Great world-building."),
            Review(movie_id=oppenheimer.id, author_name="bob", rating=5, comment="Excellent performances."),
        ])
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
