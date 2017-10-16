#! /usr/bin/python3.5.3

import json
import threading
import sys
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from cachetools import LFUCache


ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""


class Timer(object):

    def __init__(self, interval, function):
        """
        Use timer to run a function after every interval(n seconds)
        """
        self.interval = interval
        self.function = function
        self.thread = threading.Thread(target=self.run)
        # daemonize this thread, so that it allows the program to exit
        # even when a thread is running.
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            time.sleep(self.interval)
            self.function()


class TwitterListener(StreamListener):

    def __init__(self):
        self.cache = LFUCache(maxsize=50)
        self.cache2 = LFUCache(maxsize=50)
        Timer(interval=60, function=self.print_keys)
        Timer(interval=30, function=self.check_cached_words)

    def on_data(self, data):
        data_lst = json.loads(data)
        data_lst = data_lst.get('text', '').split()

        if self.cache.currsize == self.cache.maxsize:
            for key in list(self.cache.keys()):
                if self.cache[key] == 0:
                    del self.cache[key]

        for word in data_lst:
            if word in self.cache.keys():
                self.cache[word] += 1
            else:
                self.cache[word] = 1
            if self.cache[word] < 0:
                del self.cache[word]

        return True

    def print_keys(self):
        """
        print recent words and update the second cache every 60 seconds
        """
        print(list(self.cache.items()))
        self.cache2.update(self.cache)
        return True

    def check_cached_words(self):
        """
        Decrease score of word by 1 if the score does not change within
        60 seconds
        """
        for word in list(self.cache.keys()):
            if self.cache.get(word) == self.cache2.get(word):
                self.cache[word] -= 1
        return True


if __name__ == '__main__':
    keyword = input("Enter a keyword: ")
    listener = TwitterListener()

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    try:
        stream = Stream(auth=auth, listener=listener)
        stream.filter(track=[keyword], languages=["en"])
    except KeyboardInterrupt:
        stream.disconnect()
        sys.exit(0)
