# -*- coding: utf-8 -*-
# Natural Language Toolkit: Twitter client
#
# Copyright (C) 2001-2015 NLTK Project
# Author: Ewan Klein <ewan@inf.ed.ac.uk>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Examples to demo the :py:mod:`twitterclient` code.

For documentation about the Twitter APIs, see `The Streaming APIs Overview
<https://dev.twitter.com/streaming/overview>`_ and `The REST APIs Overview
<https://dev.twitter.com/rest/public>`_.
"""

from functools import wraps
import os

from twitterclient import *
from util import extract_tweetid

spacer = '###################################'

def verbose(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print()
        print(spacer)
        print("Using %s" % (func.__name__))
        print(spacer)
        return func(*args, **kwargs)
    return with_logging



TWITTER = os.environ['TWITTER']
TWEETS = os.path.join(TWITTER, 'demo_tweets.json')
IDS = os.path.join(TWITTER, 'tweet_ids.txt')
USERIDS = ['759251','612473',  '15108702',   '6017542',    '2673523800'] # UserIDs corresponding to\
#           @CNN,    @BBCNews, @ReutersLive, @BreakingNews, @AJELive
HYDRATED = os.path.join(TWITTER, 'rehydrated.json')

# demo 0
@verbose
def sampletoscreen_demo(limit=20):
    """
    Sample from the Streaming API and send output to terminal.
    """
    oauth = credsfromfile()
    client = Streamer(**oauth)
    client.register(TweetViewer(limit=limit))
    client.statuses.sample()

# demo 1
@verbose
def tracktoscreen_demo(track="taylor swift", limit=10):
    """
    Track keywords from the public Streaming API and send output to terminal.
    """
    oauth = credsfromfile()
    client = Streamer(**oauth)
    client.register(TweetViewer(limit=limit))
    client.statuses.filter(track=track)

# demo 2
@verbose
def search_demo(keywords='nltk'):
    """
    Using the REST API, search for past tweets containing a given keyword.
    """
    oauth = credsfromfile()
    client = Query(**oauth)
    for t in client.search_tweets(keywords=keywords, count=10):
        print(t['text'])

# demo 3
@verbose
def lookup_by_userid_demo():
    """
    Use the REST API to convert a userID to a screen name.
    """
    oauth = credsfromfile()
    client = Query(**oauth)
    user_info = client.user_info_from_id(USERIDS)
    for info in user_info:
        sn = info['screen_name']
        followers = info['followers_count']
        following = info['friends_count']
        print("{}, followers: {}, following: {}".format(sn, followers, following))

# demo 4
@verbose
def followtoscreen_demo(limit=10):
    """
    Using the Streaming API, select just the tweets from a specified list of
    userIDs.

    This is only likely to give quick results if the users in question
    produce a high-volume of tweets.
    """
    oauth = credsfromfile()
    client = Streamer(**oauth)
    client.register(TweetViewer(limit=limit))
    client.statuses.filter(follow=USERIDS)

# demo 5
@verbose
def streamtofile_demo(limit=20):
    """
    Write 20 tweets sampled from the public Streaming API to a file.
    """
    oauth = credsfromfile()
    client = Streamer(**oauth)
    client.register(TweetWriter(limit=limit, repeat=False))
    client.statuses.sample()

# demo 6
@verbose
def extract_tweetids_demo(infile, outfile):
    """
    Given a list of full tweets in a file (``infile``), write just the
    tweetIDs to a new file (`outfile`)
    """
    print("Reading from {}".format(infile))
    print()
    ids = extract_tweetid(infile)
    with open(outfile, 'w') as f:
        print("Writing ids to {}".format(outfile))
        print()
        for id_str in ids:
            print("Found id {}".format(id_str))
            print(id_str, file=f)

# demo 7
@verbose
def expand_tweetids_demo(infile, outfile):
    """
    Given a list of tweetIDs in a file (``infile``), try to recover the full
    ('hydrated') tweets from the REST API and write the results to a new file (`outfile`).

    If any of the tweets corresponding to the tweetIDs have been deleted by
    their authors, :meth:`lookup` will return an empty result.
    """
    oauth = credsfromfile()
    client = Query(**oauth)
    client.lookup(infile, outfile)

# demo 8
@verbose
def corpusreader_demo():
    """
    Use :module:`TwitterCorpusReader` tp read a file of tweets, and print out

    * some full tweets in JSON format;
    * some raw strings from the tweets (i.e., the value of the `text` field); and
    * the result of tokenising the raw strings.

    """
    from nltk.corpus import TwitterCorpusReader
    root = os.environ['TWITTER']
    reader = TwitterCorpusReader(root, 'rehydrated.json')
    print()
    print("Complete tweet documents")
    print(spacer)
    for t in reader.docs()[:2]:
        print(json.dumps(t, indent=1, sort_keys=True))

    print()
    print("Raw tweet strings:")
    print(spacer)
    for t in reader.strings()[:15]:
        print(t)

    print()
    print("Tokenized tweet strings:")
    print(spacer)
    for t in reader.tokenized()[:15]:
        print(t)

# demo 9
@verbose
def twitterclass_demo():
    """
    Use the simplified :class:`Twitter` class to write some tweets to a file.
    """
    tw = Twitter()
    tw.tweets(keywords='love, hate', limit=10) #public stream
    tw.tweets(keywords='love, hate', stream=False, limit=10) # search past tweets
    tw.tweets(follow=['759251','6017542'], limit=10) #public stream



all_demos = range(8)
DEMOS = all_demos
DEMOS = [9]

if __name__ == "__main__":
    """
    Run selected demo functions.
    """
    if 0 in DEMOS:
        sampletoscreen_demo()
    if 1 in DEMOS:
        tracktoscreen_demo()
    if 2 in DEMOS:
        search_demo()
    if 3 in DEMOS:
        lookup_by_userid_demo()
    if 4 in DEMOS:
        followtoscreen_demo()
    if 5 in DEMOS:
        streamtofile_demo()
    if 6 in DEMOS:
        extract_tweetids_demo(TWEETS, IDS)
    if 7 in DEMOS:
        expand_tweetids_demo(IDS, HYDRATED)
    if 8 in DEMOS:
        corpusreader_demo()
    if 9 in DEMOS:
        twitterclass_demo()

