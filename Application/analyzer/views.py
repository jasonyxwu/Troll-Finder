from django.http import JsonResponse

from rest_framework.decorators import api_view
import requests
from requests.structures import CaseInsensitiveDict
import re
from .apps import AnalyzerConfig

# Create your views here.
MAX_POST_NUMBER = 10


def evaluate(posts):
    result = True
    # TODO: invoke module to predict whether this user is a Troll based on posts
    return result


@api_view(["GET"])
def judge_user(request, username):
    if not re.match("^[A-Za-z0-9_]{1,15}$", username):
        return JsonResponse({"message": "INVALID USERNAME: The `username` query parameter value ["
                                        + username + "] does not match ^[A-Za-z0-9_]{1,15}$"})
    userid = retrieve_userid_of(username)
    if userid is None:
        return JsonResponse({"message": "USER NOT FOUND: no user called [" + username + "]"})
    posts = retrieve_post_by_id(userid=userid, max_number=MAX_POST_NUMBER)  # comment this line
    # when cannot get user posts
    if not posts:
        return JsonResponse({"userid": userid, "username": username, "message": "POSTS NOT FOUND"})
    # when threshold not provided
    if "threshold" not in request.headers:
        threshold = 0.7
        message = "SUCCESS(Threshold Not Provided, Apply Default 0.7)"
    else:
        threshold = request.headers["threshold"]
        message = "SUCCESS"
    # judge by given posts

    posts = [post["text"] for post in posts]
    results = AnalyzerConfig.model.predict(posts)
    positive_percentage = results.sum() / results.shape[0]
    isTroll = positive_percentage < threshold
    response_data = {"userid": userid, "username": username, "isTroll": bool(isTroll), "message": message}
    return JsonResponse(response_data)


def empty(request):
    return JsonResponse({"message": "This is Troll-Finder Discriminator!"})


def retrieve_userid_of(username):
    # invoke Get user by username to get the id of user
    url = "https://api.twitter.com/2/users/by/username/" + username
    headers = CaseInsensitiveDict()
    headers["Accept"] = "*/*"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAALUfjwEAAAAA0zHXuaLYwLS1bwSn1Ut0tw1VFaw" \
                               "%3DUl1NaSH4y2sousrhlwrQURkWKDUxf7algm1nYTT5LgBp9eEqnz"

    resp = requests.get(url, headers=headers)
    if 'errors' in resp.json():
        return None
    return resp.json()['data']['id']


def retrieve_post_by_id(userid, max_number):
    # invoke Get user timeline by userid
    url = "https://api.twitter.com/2/users/" + userid + "/tweets"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "*/*"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAALUfjwEAAAAA0zHXuaLYwLS1bwSn1Ut0tw1VFaw" \
                               "%3DUl1NaSH4y2sousrhlwrQURkWKDUxf7algm1nYTT5LgBp9eEqnz"
    params = {'max_results': max_number}
    resp = requests.get(url, headers=headers, params=params)
    posts = []
    if resp.json()['meta']['result_count'] != 0:
        posts = resp.json()['data']
    return posts
