import time
import datetime
    
def compare_date_eq_today(t: datetime.time):
    t_date = t
    today_date = datetime.date.today()
    if t_date.day == today_date.day and t_date.month == today_date.month and t_date.year == today_date.year:
        return True
    return False