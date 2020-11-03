import datetime
def getEffectDate(days=0, years=0):
    dalta_day = datetime.timedelta(days=days)
    dalta_year = datetime.timedelta(days=365*(years))
    now = datetime.datetime.now()
    n_days = now + dalta_day + dalta_year
    return n_days.strftime('%Y-%m-%d %H:%M:%S')

def compareDate(date1, date2):
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    return d1 >= d2

def GetNowDate():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__=='__main__':
    print(getEffectDate(years=100))