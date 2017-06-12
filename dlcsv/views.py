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


import json
import os
import csv
import urllib2
import urllib
import sys
import base64


import pyrebase

import pytz
import datetime as dt

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

    f = csv.writer(open("test.csv", "w"))
    f.writerow(["key","query", "slack_user_id", "created"])

    all_users = db.child("agents").get()
    for user in all_users.each():
        v1=user.key()
        v2=user.val()
        query= v2.get("query")
        slack_user_id=v2.get("slack_user_id")
        created=v2.get("created")
        f.writerow([v1,query,slack_user_id,created])
    return JsonResponse("/home/eisandy/downloadcsv/"+ "test" + ".csv", safe=False)


