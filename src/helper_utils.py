from datetime import datetime
import pytz


def get_current_time_stamp():
    return datetime.now(pytz.utc)
