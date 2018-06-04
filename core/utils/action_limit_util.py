import datetime

def validate_actions(user):
    thirty_miuntes = datetime.timedelta(minutes=30)
    time_now = datetime.datetime.utcnow()

    if user.cooldown_started and thirty_miuntes + user.cooldown_started < time_now:
        user.actions_performed = 0
        user.cooldown_started = None
        return True

    if user.actions_performed >= 5:
        user.cooldown_started = datetime.datetime.utcnow()
        return False

    return True