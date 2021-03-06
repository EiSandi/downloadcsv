from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404

try:
    from urllib.parse import urlparse, urlencode
except ImportError:
     from urllib2 import urlparse
     from urllib import urlencode

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import HTTPError
from tempfile import TemporaryFile
import tempfile
import json
import os
import csv
import urllib2
import urllib
import sys
import base64
import pyrebase
import boto
import boto.s3
import sys
from boto.s3.key import Key

import pytz
import datetime as dt
from boto.s3.connection import S3Connection
@csrf_exempt
def webhook(request):
    
    config = {
        "apiKey": "AIzaSyDAmHEuPpb8hD8xcjy8c3CPvdiNAQ9KCOA",
        "authDomain": "ll-office-bot.firebaseapp.com",
        "databaseURL": "https://ll-office-bot.firebaseio.com/",
        "storageBucket": "ll-office-bot.appspot.com",
        "serviceAccount": "./ll-office-bot-firebase-adminsdk-40uln-bd50528370.json"
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("team@lumenlab.asia", "teamtempo")
    db = firebase.database()
    all_users = db.child("agents").get()
    # f = csv.writer(open("test.csv", "w"))
    # f.writerow(["key","query", "slack_user_id", "created"])
    # all_users = db.child("agents").get()
    # for user in all_users.each():
    #     v1=user.key()
    #     v2=user.val()
    #     query= v2.get("query")
    #     slack_user_id=v2.get("slack_user_id")
    #     created=v2.get("created")
    #     f.writerow([v1,query,slack_user_id,created])

    import csv
    handle, fn = tempfile.mkstemp(suffix='.csv')

    with open(fn,"w") as f:
        writer=csv.writer(f)
        writer.writerow(["key","query", "slack_user_id", "created"])  
        for user in all_users.each():
            v1=user.key()
            v2=user.val()
            query= v2.get("query")
            slack_user_id=v2.get("slack_user_id")
            created=v2.get("created")
            writer.writerow([v1,query,slack_user_id,created])   
    print (fn)

    
    AWS_ACCESS_KEY_ID = os.environ['S3_KEY']
    AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET']    
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)
    bucket_name='teamtempo'
    bucket = conn.get_bucket(bucket_name)
    # bucket = conn.create_bucket(bucket_name,
    #     location=boto.s3.connection.Location.DEFAULT)    
    print 'Uploading %s to Amazon S3 bucket %s' % \
       (fn, bucket_name)

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    # k = Key(bucket)
    # # k.key = datetime.datetime.now()
    
    key_name =str(dt.datetime.now())
    path = 'reports'
    full_key_name = os.path.join(path, key_name)
    k = bucket.new_key(full_key_name)
    k.set_contents_from_filename(fn,
    cb=percent_cb, num_cb=10)

    return JsonResponse("done", safe=False)
# write in the existing manual csv file--------------------------------------------------------------
# config = {
#         "apiKey": "AIzaSyDAmHEuPpb8hD8xcjy8c3CPvdiNAQ9KCOA",
#         "authDomain": "ll-office-bot.firebaseapp.com",
#         "databaseURL": "https://ll-office-bot.firebaseio.com/",
#         "storageBucket": "ll-office-bot.appspot.com",
#         "serviceAccount": "./ll-office-bot-firebase-adminsdk-40uln-bd50528370.json"
#     }
#     firebase = pyrebase.initialize_app(config)
#     auth = firebase.auth()
#     user = auth.sign_in_with_email_and_password("team@lumenlab.asia", "teamtempo")
#     db = firebase.database()

#     f = csv.writer(open("test.csv", "w"))
#     f.writerow(["key","query", "slack_user_id", "created"])

#     all_users = db.child("agents").get()
#     for user in all_users.each():
#         v1=user.key()
#         v2=user.val()
#         query= v2.get("query")
#         slack_user_id=v2.get("slack_user_id")
#         created=v2.get("created")
#         f.writerow([v1,query,slack_user_id,created])
#     return JsonResponse("https://raw.githubusercontent.com/EiSandi/downloadcsv/master/"+ "test" + ".csv", safe=False)


