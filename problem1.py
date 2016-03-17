import json
import time
from feature_extract import feature_extract
import matplotlib.pyplot as plt
import numpy as np

HOUR_INDEX = 3
MINUTE_INDEX = 4
SECOND_INDEX = 5

# #SuperBowl
superbowl = '../tweet_data/tweets_#superbowl.txt'
# #NFL
nfl = '../tweet_data/tweets_#nfl.txt'

""" histogram function"""
def plot_tweet_flow(f, hashtag):
    line = f.readline()
    tweet = json.loads(line)

    start_time = list(time.localtime(tweet['firstpost_date']))
    start_time[MINUTE_INDEX] = 0; start_time[SECOND_INDEX] = 0
    nth_hour = start_time[HOUR_INDEX]
    start_time = time.mktime(start_time)
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

    timespan = 3600
    maxtime = start_time + timespan
    print maxtime
    n_tweets = 0
    history = []
    hours = []

    while len(line) != 0:
        tweet = json.loads(line)
        line = f.readline()
        tweet_time = tweet['firstpost_date']
        if tweet_time < maxtime:
            n_tweets += 1
        else:
            print "Finished %d tweets before %s" % (n_tweets, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(maxtime)))
            history.append(n_tweets)
            hours.append(nth_hour)
            n_tweets = 0
            nth_hour = (nth_hour + 1) % 24
            assert nth_hour == time.localtime(maxtime).tm_hour
            maxtime += timespan
    np.savetxt('data/'+hashtag+'histogram', history)
    np.savetxt('data/'+hashtag+'histogramlabel', hours)
    plt.bar(hours, history)
    plt.title(hashtag+' Hourly Tweet Count')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Tweets')

    plt.xticks(range(len(hours))[::12], hours[::12])
    plt.show()
    plt.savefig('graphs/'+hashtag+'tweet_count_histogram')
    plt.close()

""" end of histogram function """

print "Processing #superbowl"
f_handle = open(superbowl)
plot_tweet_flow(f_handle, '#SuperBowl')
f_handle.close()

print "Processing #nfl"
f_handle = open(nfl)
plot_tweet_flow(f_handle, '#NFL')
f_handle.close()
