import time
import datetime
import requests
import pandas as pd
import csv
first_date = '1577836800'
last_date = '1577923200'
three_month_subreddits = []

while True:
    base_url = f"https://api.pushshift.io/reddit/submission/search/?before={last_date}&after={first_date}&fields=created_utc,author,title,num_comments,url,upvote,score&size=500&limit=1000&sort=desc&subreddit=emacs"
    print(base_url)
    res = requests.get(base_url)
    if res.status_code == 200:
        re = res.json()
        subreddits = re['data']
        print(len(subreddits))
        if not subreddits:
            break
        first_date = last_date

        if int(first_date) > 1585612798:
            break
        last_date = subreddits[0]['created_utc']
        print(datetime.datetime.utcfromtimestamp(int(last_date)).strftime('%Y-%m-%d %H:%M:%S'))
        last_date = datetime.datetime.utcfromtimestamp(int(last_date))

        last_date += datetime.timedelta(days=1)

        print(last_date)

        last_date = last_date.timestamp()
        last_date = str(int(last_date))

        [three_month_subreddits.append(i) for i in subreddits]
        print(len(three_month_subreddits))
    if len(three_month_subreddits) == 50:
        break
    else:
        time.sleep(1)

with open('reddit.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = three_month_subreddits[0].keys() )
    writer.writeheader()
    writer.writerows(three_month_subreddits)

df = pd.read_csv('reddit.csv',encoding='utf8')
df["num_comments"].plot()