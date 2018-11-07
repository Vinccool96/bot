# python MILBitchBot2/MILBitchBot2.py --env --cron
import os
import praw
import psaw
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'),
                     user_agent=os.environ.get('AGENT'), password=os.environ.get('REDDIT_PASS'),
                     username=os.environ.get('REDDIT_USER'))

subreddit = reddit.subreddit('dataisbeautiful')

timenow = datetime.datetime.now()
time = int((datetime.datetime(2013, 2, 16)).timestamp())
api = psaw.PushshiftAPI(reddit)
lis = list(api.search_submissions(subreddit='dataisbeautiful', filter=['url', 'author', 'title', 'subreddit'],
                                  limit=100000000000000))

print('lis is done')

trmv = list()

tmstp = list()

score = list()

dts = list()

for subms in lis:
    if subms.author is None:
        trmv.append(subms)

print(str(len(trmv)) + ' to remove')

print('total:', len(lis))

for s in trmv:
    lis.remove(s)

print('lis is cleared, with ' + str(len(lis)) + ' posts left')
last_utc = lis[-1].created_utc

for s in lis:
    tmstp.append(s.created_utc)
    score.append(s.score)

print('data has been created')

for tm in tmstp:
    dts.append(datetime.datetime.fromtimestamp(tm))


def to_unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000


rng = list()

rng.append(to_unix_time(dts[-1]))
rng.append(to_unix_time(dts[0]))

print(rng)

plotly.tools.set_credentials_file(username=os.environ.get('PLOTLY_USERNAME'), api_key=os.environ.get('PLOTLY_KEY'))

data = [go.Scatter(x=dts, y=score)]

layout = go.Layout(xaxis=dict(range=rng))

fig = go.Figure(data=data, layout=layout)
py.plot(fig)
