"""Idempotent seed loader — populates the DB with ~40 curated movies.

Idempotency: exits immediately if any Genre rows exist.
Run via: python -m app.seed  or  make seed
"""
from __future__ import annotations

import structlog
from sqlalchemy import select

from app.db import Base, SessionLocal, engine
from app.logging_config import configure_logging
from app.models import Actor, Director, Genre, Movie, Review

configure_logging()
logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------------------

GENRES = [
    ("Action", "action"),
    ("Adventure", "adventure"),
    ("Animation", "animation"),
    ("Biography", "biography"),
    ("Comedy", "comedy"),
    ("Crime", "crime"),
    ("Documentary", "documentary"),
    ("Drama", "drama"),
    ("Fantasy", "fantasy"),
    ("History", "history"),
    ("Horror", "horror"),
    ("Music", "music"),
    ("Mystery", "mystery"),
    ("Romance", "romance"),
    ("Sci-Fi", "sci-fi"),
    ("Thriller", "thriller"),
    ("War", "war"),
]

DIRECTORS: list[tuple[str, int | None, str | None]] = [
    ("Christopher Nolan", 1970, "British-American director known for cerebral, nonlinear storytelling."),
    ("Denis Villeneuve", 1967, "French Canadian director acclaimed for visually striking science fiction."),
    ("Greta Gerwig", 1983, "American director and screenwriter."),
    ("Bong Joon-ho", 1969, "South Korean director, screenwriter, and producer."),
    ("Kathryn Bigelow", 1951, "American director and producer."),
    ("Quentin Tarantino", 1963, "American director and screenwriter known for stylized violence."),
    ("David Fincher", 1962, "American director known for dark psychological thrillers."),
    ("Martin Scorsese", 1942, "American director, producer, and screenwriter."),
    ("Steven Spielberg", 1946, "American director, producer, and screenwriter."),
    ("Wes Anderson", 1969, "American director known for symmetrical compositions and quirky style."),
    ("Hayao Miyazaki", 1941, "Japanese animator and director, co-founder of Studio Ghibli."),
    ("Jordan Peele", 1979, "American director known for socially conscious horror."),
    ("Alfonso Cuarón", 1961, "Mexican director, screenwriter, and producer."),
    ("Ridley Scott", 1937, "British director known for epic science fiction and drama."),
    ("Damien Chazelle", 1985, "American director known for music-driven dramas."),
    ("Ari Aster", 1986, "American director known for psychological horror."),
    ("Park Chan-wook", 1963, "South Korean director known for his Vengeance trilogy."),
    ("Sofia Coppola", 1971, "American director and screenwriter."),
]

# (name, birth_year, bio)
ACTORS: list[tuple[str, int | None, str | None]] = [
    ("Leonardo DiCaprio", 1974, "American actor and film producer."),
    ("Cate Blanchett", 1969, "Australian actress and theatre director."),
    ("Tom Hanks", 1956, "American actor and filmmaker."),
    ("Meryl Streep", 1949, "American actress widely regarded as the greatest of her generation."),
    ("Denzel Washington", 1954, "American actor, director, and producer."),
    ("Joaquin Phoenix", 1974, "American actor known for his intense character transformations."),
    ("Saoirse Ronan", 1994, "Irish-American actress."),
    ("Timothée Chalamet", 1995, "American-French actor."),
    ("Zendaya", 1996, "American actress and singer."),
    ("Florence Pugh", 1996, "British actress."),
    ("Christian Bale", 1974, "British actor known for dramatic physical transformations."),
    ("Anne Hathaway", 1982, "American actress and singer."),
    ("Matthew McConaughey", 1969, "American actor and producer."),
    ("Jessica Chastain", 1977, "American actress and producer."),
    ("Brad Pitt", 1963, "American actor and film producer."),
    ("Margot Robbie", 1990, "Australian actress and producer."),
    ("Ryan Gosling", 1980, "Canadian actor and musician."),
    ("Emma Stone", 1988, "American actress."),
    ("Michael B. Jordan", 1987, "American actor and filmmaker."),
    ("Lupita Nyong'o", 1983, "Mexican-Kenyan actress."),
    ("Daniel Kaluuya", 1989, "British actor and screenwriter."),
    ("Toni Collette", 1972, "Australian actress and singer."),
    ("Hugh Jackman", 1968, "Australian actor and producer."),
    ("Robert De Niro", 1943, "American actor, producer, and director."),
    ("Al Pacino", 1940, "American actor and filmmaker."),
    ("Joe Pesci", 1943, "American actor and musician."),
    ("Uma Thurman", 1970, "American actress and model."),
    ("Samuel L. Jackson", 1948, "American actor and producer."),
    ("John Travolta", 1954, "American actor and singer."),
    ("Tilda Swinton", 1960, "British actress."),
    ("Bill Murray", 1950, "American actor, comedian, and writer."),
    ("Ralph Fiennes", 1962, "British actor and director."),
    ("Charlize Theron", 1975, "South African and American actress and producer."),
    ("Anya Taylor-Joy", 1996, "British-American actress."),
    ("Oscar Isaac", 1979, "Guatemalan-American actor."),
    ("Scarlett Johansson", 1984, "American actress."),
    ("Mahershala Ali", 1974, "American actor."),
    ("Frances McDormand", 1957, "American actress and producer."),
    ("Adam Driver", 1983, "American actor."),
    ("Lily Gladstone", 1986, "American actress."),
    ("Michelle Yeoh", 1962, "Malaysian actress."),
    ("Ke Huy Quan", 1971, "Vietnamese-American actor."),
    ("Gary Oldman", 1958, "British actor and filmmaker."),
    ("Tom Hardy", 1977, "British actor and producer."),
    ("Rooney Mara", 1985, "American actress."),
    ("Matt Damon", 1970, "American actor, producer, and screenwriter."),
    ("Joseph Gordon-Levitt", 1981, "American actor, filmmaker, and entrepreneur."),
    ("Marion Cotillard", 1975, "French actress and singer."),
    ("Cillian Murphy", 1976, "Irish actor."),
    ("Stellan Skarsgård", 1951, "Swedish actor."),
    ("Rebecca Ferguson", 1983, "Swedish actress."),
    ("Viola Davis", 1965, "American actress and producer."),
    ("Casey Affleck", 1975, "American actor, director, and producer."),
    ("Andrew Garfield", 1983, "British-American actor."),
]

# (title, year, director_idx, genre_slugs, actor_indices, synopsis, runtime, ratings)
MOVIES_DATA: list[tuple] = [
    (
        "Inception", 2010, 0,
        ["action", "sci-fi", "thriller"],
        [0, 46, 47, 11],
        "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        148, [5, 5, 4, 5],
    ),
    (
        "The Dark Knight", 2008, 0,
        ["action", "crime", "drama"],
        [10, 42],
        "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        152, [5, 5, 5, 4, 5],
    ),
    (
        "Interstellar", 2014, 0,
        ["adventure", "drama", "sci-fi"],
        [12, 11],
        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        169, [5, 4, 5],
    ),
    (
        "Dune", 2021, 1,
        ["adventure", "drama", "sci-fi"],
        [7, 8, 34, 49, 50],
        "Feature adaptation of Frank Herbert's science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset in the galaxy.",
        155, [5, 4, 5],
    ),
    (
        "Arrival", 2016, 1,
        ["drama", "mystery", "sci-fi"],
        [13, 38],
        "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.",
        116, [5, 5],
    ),
    (
        "Blade Runner 2049", 2017, 1,
        ["action", "drama", "sci-fi"],
        [16, 5],
        "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard.",
        163, [4, 5],
    ),
    (
        "Lady Bird", 2017, 2,
        ["comedy", "drama"],
        [6],
        "In Sacramento in 2002, a high school senior navigates her senior year alongside her complicated relationship with her mother.",
        94, [5, 4],
    ),
    (
        "Little Women", 2019, 2,
        ["drama", "romance"],
        [6, 9, 10, 15],
        "Jo March reflects back and recounts to her sisters how they came of age during and after the Civil War.",
        135, [5, 5, 4],
    ),
    (
        "Barbie", 2023, 2,
        ["adventure", "comedy", "fantasy"],
        [15, 16],
        "Barbie suffers a crisis that leads her to question her world and her existence.",
        114, [4, 5, 4],
    ),
    (
        "Parasite", 2019, 3,
        ["comedy", "drama", "thriller"],
        [],
        "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        132, [5, 5, 5],
    ),
    (
        "The Hurt Locker", 2008, 4,
        ["drama", "thriller", "war"],
        [],
        "During the Iraq War, a Sergeant recently assigned to an army bomb squad is at odds with his squad mates due to his maverick way of handling his work.",
        131, [4, 5],
    ),
    (
        "Pulp Fiction", 1994, 5,
        ["crime", "drama"],
        [26, 27, 28],
        "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        154, [5, 5, 5, 5],
    ),
    (
        "Kill Bill: Vol. 1", 2003, 5,
        ["action", "crime", "thriller"],
        [26],
        "After awakening from a four-year coma, a woman seeks vengeance against the assassination squad who nearly killed her and her unborn child.",
        111, [4, 5],
    ),
    (
        "Once Upon a Time in Hollywood", 2019, 5,
        ["comedy", "drama"],
        [14, 15],
        "A faded television actor and his stunt double strive to achieve fame and success in the final years of Hollywood's Golden Age in 1969 Los Angeles.",
        161, [4, 4, 5],
    ),
    (
        "Fight Club", 1999, 6,
        ["drama", "thriller"],
        [14, 23],
        "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more sinister.",
        139, [5, 5, 4],
    ),
    (
        "Gone Girl", 2014, 6,
        ["drama", "mystery", "thriller"],
        [38, 44],
        "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent.",
        149, [4, 4],
    ),
    (
        "The Social Network", 2010, 6,
        ["biography", "drama"],
        [45, 17],
        "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea and his best friend who was later squeezed out of the business.",
        120, [4, 5],
    ),
    (
        "Goodfellas", 1990, 7,
        ["biography", "crime", "drama"],
        [23, 25],
        "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
        146, [5, 5, 5],
    ),
    (
        "The Wolf of Wall Street", 2013, 7,
        ["biography", "comedy", "crime"],
        [0, 48, 46],
        "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.",
        180, [4, 4, 4],
    ),
    (
        "Killers of the Flower Moon", 2023, 7,
        ["crime", "drama", "history"],
        [0, 23, 39],
        "Members of the Osage Nation are murdered under mysterious circumstances in the 1920s, sparking a major FBI investigation involving J. Edgar Hoover.",
        206, [4, 5],
    ),
    (
        "Saving Private Ryan", 1998, 8,
        ["drama", "war"],
        [2],
        "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        169, [5, 5],
    ),
    (
        "The Grand Budapest Hotel", 2014, 9,
        ["adventure", "comedy", "drama"],
        [31, 30, 29],
        "A writer encounters the owner of an aging European hotel who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
        99, [5, 5, 4],
    ),
    (
        "Spirited Away", 2001, 10,
        ["animation", "adventure", "fantasy"],
        [],
        "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits.",
        125, [5, 5, 5],
    ),
    (
        "Princess Mononoke", 1997, 10,
        ["action", "adventure", "animation", "fantasy"],
        [],
        "On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony.",
        134, [5, 4],
    ),
    (
        "Get Out", 2017, 11,
        ["horror", "mystery", "thriller"],
        [20, 19],
        "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.",
        104, [5, 5, 4],
    ),
    (
        "Nope", 2022, 11,
        ["horror", "mystery", "sci-fi"],
        [20, 8],
        "The residents of a lonely gulch in inland California bear witness to an uncanny and chilling discovery.",
        130, [4, 4],
    ),
    (
        "Roma", 2018, 12,
        ["drama"],
        [],
        "A year in the life of a middle-class family's indigenous housekeeper in Colonia Roma, Mexico City.",
        135, [5],
    ),
    (
        "Children of Men", 2006, 12,
        ["action", "drama", "sci-fi", "thriller"],
        [43],
        "In 2027, in a chaotic world in which women have become somehow infertile, a former activist agrees to help transport a miraculously pregnant woman to a sanctuary at sea.",
        109, [5, 5],
    ),
    (
        "Gladiator", 2000, 13,
        ["action", "adventure", "drama"],
        [],
        "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        155, [5, 5],
    ),
    (
        "The Martian", 2015, 13,
        ["adventure", "drama", "sci-fi"],
        [45],
        "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.",
        144, [5, 4],
    ),
    (
        "La La Land", 2016, 14,
        ["comedy", "drama", "music", "romance"],
        [16, 17],
        "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        128, [5, 5, 4],
    ),
    (
        "Whiplash", 2014, 14,
        ["drama", "music"],
        [53],
        "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
        106, [5, 5],
    ),
    (
        "Hereditary", 2018, 15,
        ["drama", "horror", "mystery"],
        [21],
        "When the matriarch of the Graham family passes away, her daughter's family begins to unravel cryptic and terrifying secrets about their ancestry.",
        127, [5, 4],
    ),
    (
        "Midsommar", 2019, 15,
        ["drama", "horror", "mystery"],
        [9],
        "A couple travels to Northern Europe to visit a rural hometown's fabled Swedish midsummer festival. What begins as an idyllic retreat quickly devolves into an increasingly violent competition.",
        148, [4, 4],
    ),
    (
        "Oldboy", 2003, 16,
        ["action", "drama", "mystery", "thriller"],
        [],
        "After being inexplicably imprisoned for 15 years, Oh Dae-su is released, only to find he must find his captor in five days.",
        120, [5, 5],
    ),
    (
        "Lost in Translation", 2003, 17,
        ["comedy", "drama", "romance"],
        [30, 35],
        "A faded movie star and a neglected young woman form an unlikely bond after crossing paths in Tokyo.",
        102, [4, 5],
    ),
    (
        "Everything Everywhere All at Once", 2022, None,
        ["action", "adventure", "comedy", "sci-fi"],
        [40, 41],
        "An aging Chinese immigrant is swept up in an insane adventure in which she alone can save the world by exploring other universes connecting with the lives she could have led.",
        139, [5, 5, 5],
    ),
    (
        "Oppenheimer", 2023, 0,
        ["biography", "drama", "history"],
        [48, 16, 38],
        "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
        180, [5, 5, 4],
    ),
    (
        "Joker", 2019, None,
        ["crime", "drama", "thriller"],
        [5],
        "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.",
        122, [4, 5, 4],
    ),
    (
        "The Silence of the Lambs", 1991, None,
        ["crime", "drama", "horror", "thriller"],
        [51],
        "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
        118, [5, 5, 5],
    ),
]


def _canned_comment(rating: int) -> str:
    return {
        5: "Absolutely brilliant. A must-watch masterpiece.",
        4: "Really enjoyed this — well worth the time.",
        3: "Solid film with some memorable moments.",
        2: "Had its issues but still watchable.",
        1: "Not for me, unfortunately.",
    }.get(rating, "Worth a watch.")


def load_seed(db) -> dict:  # type: ignore[type-arg]
    """Idempotent seed: if any Genre rows exist, do nothing."""
    if db.scalar(select(Genre.id).limit(1)) is not None:
        logger.info("seed_skipped", reason="already seeded")
        return {"genres": 0, "directors": 0, "actors": 0, "movies": 0, "reviews": 0}

    genres = [Genre(name=name, slug=slug) for name, slug in GENRES]
    directors = [Director(name=n, birth_year=y, bio=b) for n, y, b in DIRECTORS]
    actors = [Actor(name=n, birth_year=y, bio=b) for n, y, b in ACTORS]
    db.add_all(genres + directors + actors)
    db.flush()

    by_slug = {g.slug: g for g in genres}
    review_count = 0

    for title, year, dir_idx, genre_slugs, actor_idxs, synopsis, runtime, ratings in MOVIES_DATA:
        movie_genres_list = [by_slug[s] for s in genre_slugs if s in by_slug]
        movie_actors_list = [actors[i] for i in actor_idxs if i < len(actors)]
        director = directors[dir_idx] if dir_idx is not None and dir_idx < len(directors) else None
        avg = sum(ratings) / len(ratings) if ratings else None
        movie = Movie(
            title=title,
            release_year=year,
            director=director,
            genres=movie_genres_list,
            actors=movie_actors_list,
            synopsis=synopsis,
            runtime_minutes=runtime,
            average_rating=avg,
        )
        db.add(movie)
        db.flush()
        for i, r in enumerate(ratings):
            db.add(Review(
                movie_id=movie.id,
                author_name=f"Reviewer{i + 1}",
                rating=r,
                comment=_canned_comment(r),
            ))
            review_count += 1

    db.commit()
    counts = {
        "genres": len(genres),
        "directors": len(directors),
        "actors": len(actors),
        "movies": len(MOVIES_DATA),
        "reviews": review_count,
    }
    logger.info("seed_loaded", **counts)
    return counts


def seed() -> None:
    """Entry point used by Dockerfile CMD and make seed."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        load_seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
