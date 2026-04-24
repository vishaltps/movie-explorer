from app.models import Actor, Director, Genre, Movie, Review


def test_model_relationships_round_trip(db_session):
    genre = Genre(name="Mystery", slug="mystery")
    director = Director(name="Jane Campion", birth_year=1954, bio="Director bio")
    actor = Actor(name="Benedict Cumberbatch", birth_year=1976, bio="Actor bio")
    movie = Movie(
        title="The Power of the Dog",
        release_year=2021,
        synopsis="A tense character drama.",
        runtime_minutes=126,
        director=director,
        genres=[genre],
        actors=[actor],
        average_rating=4.0,
    )
    review = Review(movie=movie, author_name="critic", rating=4, comment="Excellent")

    db_session.add_all([genre, director, actor, movie, review])
    db_session.commit()
    db_session.refresh(movie)

    assert movie.director is not None
    assert movie.director.name == "Jane Campion"
    assert movie.genres[0].name == "Mystery"
    assert movie.actors[0].name == "Benedict Cumberbatch"
    assert movie.reviews[0].author_name == "critic"
