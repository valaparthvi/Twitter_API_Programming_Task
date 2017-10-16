### Task
Use the Twitter Streaming API to track a given keyword and maintain a cache of most recently used words.

The words in cache are scored as following:
- Every time a word is seen, it’s score goes up by 1.
- Every minute the word is not seen, it’s score goes down by 1. This scoringis done every 30 seconds.

Once the score of a word falls below 0, it is pruned from the cache.

New entries in the cache have score 1. If the cache has reached maximum size,words with score 0 can be dropped to make space for new entries.

### Input
- keyword (program should prompt on the command line)
### Output
- After starting, every 1 minute, program should print the words in cache with score > 1.

### Requirements
  1. Install **tweepy** : `sudo pip3 install tweepy`
  2. Install **cachetools**: `sudo pip3 install cachetools`
  2. Obtain and set the following variables:
    - CONSUMER_KEY
    - CONSUMER_SECRET
    - ACCESS_KEY
    - ACCESS_SECRET
  
### Running the script
  1. Set the values of above mentioned variables in the script.
  2. Run the script `python3 tweepy_stream_listener.py`

### Approach
There are 5 main tasks to be carried out:
  1. Connect to Twitter's streaming API.
  2. Continuously score the words as they are received
  3. Printing the words inside cache every 60 seconds
  4. Decrease the score of words by 1, words whose value does not change within 60 seconds. Carry out this task every 30 seconds.
  5. Set a timer to carry out the tasks 3 and 4 after every 60 and 30 seconds. 

  #### Task 1
    1. Create a class inheriting from StreamListener
    2. Using that class create a Stream object (`TwitterListener`)
    3. Connect to the Twitter API using the Stream.
  #### Task 2
    1. Load the the data into json format, and create a list of words used in a "text".
    2. Check if the cache has reached it's maximum size. If yes, then delete the words whose score is 0.
    3. Loop through the list of newly received words. If a words exists in the cache, then incremeant it's score by 1. Else, add the word to cache with initial score 1.
  #### Task 3 and 4
    1. Create two methods: 1) print_keys and 2) check_cached_words inside 'TwitterListener'.
    2. We use 2 caches here. One cache is used to maintain the continuously incoming data. A second cache is maintained to check if the score of a word has changed. This second cache is updated after every 60 seconds.
    3. In check_cached_words, check if the value of a score has changed in the last 60 seconds, if it has not changed, then decreament it by 1.
    4. In print_keys, print the words inside cache every 60 seconds and update the second cache.
  #### Task 5
    1. Create a class Timer, that allows to run a certain functions after every 'n' seconds.
    2. 2 Timer objects are initialized when the 'TwitterListener' is initialized, one for print_keys and another for check_cached_words.

### Tools used
  1. [Tweepy](https://github.com/tweepy/tweepy) - An easy-to-use Python library for accessing the Twitter API.
  2. [cachetools](https://pypi.python.org/pypi/cachetools) - Extensible memoizing collections and decorators
### Resources
  1. [Tweepy Docs](http://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html "tweepy docs")
  2. [cachetools Docs](http://cachetools.readthedocs.io/en/latest/#cachetools.LFUCache)
  3. [Running-a-method-as-a-background-thread-in-python](http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/)
