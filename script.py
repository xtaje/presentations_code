from __future__ import print_function
import config
import boto3
import cStringIO

STOCK_SYMBOLS=["MMM", "GOOG", "NFLX"] # and so on ...
THRESHOLD = 0.5

def find_bad_articles(bucket_name, batch_size=100):
    objects = fetch_objects(bucket_name, batch_size)
    for obj in objects:
        buf = cStringIO.StringIO()
        obj.downloadfileobj(buf) # What to do about this?
        words = buf.getvalue().split()

        limit = THRESHOLD * len(words)
        for w in words:
            if w in STOCK_SYMBOLS:
               limit -=1 

            if limit <= 0:
                yield obj.key # and what to do about this?

def fetch_objects(bucket_name, batch_size):
    s3 = boto3.resource('s3', config.aws_key, config.aws_secret)
    objects = s3.Bucket(bucket_name).objects
    return objects.page_size(batch_size)