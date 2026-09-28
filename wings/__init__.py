from . import cinema_quiz, movie_facts, movie_recommendations

WINGS = {
    w.NAME: w
    for w in (movie_facts, cinema_quiz, movie_recommendations)
}
