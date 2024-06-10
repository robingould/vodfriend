from datetime import datetime

def get_time():
    current_time = datetime.now()
    format = '%I:%M %p'   
    time_now = current_time.strftime(format)
    return time_now

def get_date():
    current_time = datetime.now()
    format = '%m/%d/%Y' 
    todays_date = current_time.strftime(format)
    return todays_date
