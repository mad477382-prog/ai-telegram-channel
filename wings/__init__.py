from . import daily_poll, daily_quiz, shocking_fact

WINGS = {
    w.NAME: w
    for w in (daily_quiz, shocking_fact, daily_poll)
}
