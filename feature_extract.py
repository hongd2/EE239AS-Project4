import json
import time
from datetime import date

HOUR_INDEX = 3
MINUTE_INDEX = 4
SECOND_INDEX = 5

def feature_extract(f, o_file):
    import json
    import time
    from datetime import date

    line = f.readline()
    tweet = json.loads(line)

    n_tweets = 0 # number of tweets per hour
    n_followers = {} # uid -> (nfollower, ntweets) per hour
    n_retweets = 0 # number of retweets per hour
    num_window = 0 # total number of hours

    user_follower = {}

    # self defined features (for part 2)
    # n_users:-  number of users tweeted per hour
    # n_users_3:- number of users who tweeted 3 times or more per hour
    n_len_100 = 0 # number of tweets with more than 100 characters per hour

    # outputs
    import numpy as np

    """
    output: n_tweets  n_retweets  sum_followers  max_followers  hour \
            avg_tweet_per_user  n_users  n_users_3  n_len_100
    """
    output = np.empty([0, 9])

    # get start hour from first tweet
    start_time = list(time.localtime(tweet['firstpost_date']))
    start_time[MINUTE_INDEX] = 0; start_time[SECOND_INDEX] = 0
    nth_hour = start_time[HOUR_INDEX]
    start_time = time.mktime(start_time)
    start_date = date.fromtimestamp(start_time)
    print "Starting from time %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

    time_format = "%Y-%m-%d %H:%M:%S"

    while len(line) != 0:
        tweet = json.loads(line)
        line = f.readline()
        tweet_time = tweet['firstpost_date']
        tweet_hour = time.localtime(tweet_time).tm_hour
        if tweet_hour != nth_hour or start_date != date.fromtimestamp(float(tweet_time)):
            print "Finished processing %d tweets from hour %d, next date time %s" %\
                  (n_tweets, nth_hour, time.strftime(time_format, time.localtime(tweet_time)))
            # update output
            tweets_per_user = np.array(n_followers.values())[:, 1]
            new_hour = np.array([[n_tweets, n_retweets, sum(n_followers), max(n_followers), nth_hour \
                                  np.mean(tweets_per_user), len(n_followers), sum(tweets_per_user >= 3) \
                                  n_len_100]])
            output = np.append(output, new_hour, axis=0)
            # clear & update hourly variables
            num_window += 1
            n_tweets = 0 # number of tweets per hour
            n_followers = {} # number of followers of users posting the tweets per hour
            n_retweets = 0 # number of retweets per hour
            nth_hour = tweet_hour  # hour of the day
            n_len_100 = 0

        # extract features
        n_tweets += 1
        n_retweets += tweet['tweet']['retweet_count']
        if tweet['tweet']['user']['id'] in n_followers:
            # increment user tweet count
            tweet_count = n_followers[tweet['tweet']['user']['id']][1] + 1
            n_followers[tweet['tweet']['user']['id']] = (tweet['tweet']['user']['followers_count'], tweet_count)
        else:
            n_followers[tweet['tweet']['user']['id']] = (tweet['tweet']['user']['followers_count'], 1)
        if (len(tweet['tweet']['text']) >= 100): n_len_100 += 1
        user_follower[tweet['tweet']['user']['id']] = tweet['tweet']['user']['followers_count']
        start_date = date.fromtimestamp(float(tweet_time))

    print "Outputting to '%s' ..." % o_file
    with open('data/' + o_file, 'w') as of:
        np.savetxt(o_file, output, delimiter=',')

    print "--------------------"
    print "Total number of tweets %d" % int(np.sum(output[:, 0]))
    print "Average number of tweets per hour %f" % np.mean(output[:, 0])
    print "Average number of retweets %f" % float(np.sum(output[:, 1]) / np.sum(output[:, 0]))
    print "Average number of followers of (%d) users %f" %\
          (len(user_follower), float(sum(user_follower.values()) / float(len(user_follower))))

# from os import listdir
#
# HOUR_INDEX = 3
# MINUTE_INDEX = 4
# SECOND_INDEX = 5
#
# files = listdir('../tweet_data')
# print files
# from os.path import splitext
#
# import re
#
# for fname in files:
#     m = re.search('#.+', splitext(files[0])[0])
#     if m:
#         hashtag = m.group()
#         print "Processing '%s'" % hashtag
#     outfile = splitext(fname)[0] + '.csv'
#     print "Output file name '%s'" % outfile
#
#     f_handle = open('../tweet_data/'+fname)
#     feature_extract(f_handle, outfile)
#     f_handle.close()
#     break;
