from os import environ
from os.path import expanduser

HOME = expanduser('~/.alphakt')
reddit_secret = environ['REDDIT_SECRET']
client_id = environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"
POSTS_PER_MINUTE = 500  # This is way beyond my estimate but it worked for my test of 10 to 15 min

access_credentials = {
    'access_token': environ['ACCESS_TOKEN'],
    'refresh_token': environ['REFRESH_TOKEN'],
    'scope': {'read'}
}


child_directories = (
    'fresh',
    '1hr', '2hr', '3hr', '4hr',
    '5hr', '6hr', '7hr', '8hr',
)

input_columns = (
    "quarantine",  # true/false -> 0/1

    "domain",  # str -> int
    "hidden",  # true/false -> 0/1

    # "author",  # str
    "num_reports",  # int -> int (normalize)
    "stickied",  # bool -> 0/1
    "gilded",  # bool -> 0/1
    "created_seconds_since_midnight",  # int -> int (change to hours)
    "created_day_of_week",  # int -> int

    "ups",  # int -> int (normalize)
    "downs",  # int -> int (normalize)
    "score",  # int -> int (normalize)
    "subreddit",  # str -> int
    "over_18",  # bool -> 0/1
    "locked",  # bool -> 0/1
    "distinguished",  # ''/'moderator'/'admin'/'special' -> 0/1/2/3
    "num_comments",  # int -> int (normalize)
    "edited",  # bool -> 0/1
    "author_flair_text",
    "link_flair_text",

    "1hr_score",  # int -> int (normalize)
    "1hr_ups",  # int -> int (normalize)
    "1hr_downs",  # int -> int (normalize)
    "1hr_num_comments",  # int -> int (normalize)
    "1hr_gilded",  # bool -> 0/1
    "1hr_num_reports",  # int -> int (normalize)
    "1hr_locked",  # bool -> 0/1
    "1hr_edited",  # bool -> 0/1

    "2hr_score",
    "2hr_ups",
    "2hr_downs",
    "2hr_num_comments",
    "2hr_gilded",
    "2hr_num_reports",
    "2hr_locked",
    "2hr_edited",
)

nominal_columns = (
    "domain",
    "subreddit",
)

normalized_columns = (
    "num_reports",
    "ups",
    "downs",
    "score",
    "num_comments",

    "1hr_score",
    "1hr_ups",
    "1hr_ups",
    "1hr_downs",
    "1hr_num_comments",
    "1hr_num_reports",

    "2hr_score",
    "2hr_ups",
    "2hr_ups",
    "2hr_downs",
    "2hr_num_comments",
    "2hr_num_reports",

)


def next_dir(current):
    if current == child_directories[-1]:
        return None
    return child_directories[child_directories.index(current) + 1]
