from . import daily_quiz
from . import shocking_fact
from . import daily_poll
from . import movie_recommendations

WINGS = {
    daily_quiz.NAME: daily_quiz,
    shocking_fact.NAME: shocking_fact,
    daily_poll.NAME: daily_poll,
    movie_recommendations.NAME: movie_recommendations,
}
