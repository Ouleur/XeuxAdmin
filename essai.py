from datetime import datetime, timedelta

date1 = datetime.strptime('2022-03-21', '%Y-%m-%d')

date2 = datetime.strptime('2022-03-23', '%Y-%m-%d')

count = date2 + timedelta(days=1)

print(count)

