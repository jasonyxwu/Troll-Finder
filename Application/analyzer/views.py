from django.http import JsonResponse

from rest_framework.decorators import api_view
import requests
from requests.structures import CaseInsensitiveDict

# Create your views here.
MAX_POST_NUMBER = 10


def evaluate(posts):
    result = True
    # TODO: invoke module to predict whether this user is a Troll based on posts
    return result


@api_view(["GET"])
def judge_user(request, username):
    # TODO: use userid to get user information, store the latest posts in variable posts: String[]
    if username == "":
        return JsonResponse({"message": "INVALID USERNAME"})

    userid = retrieve_userid_of(username)
    posts = retrieve_post_by_id(userid=userid, max_number=MAX_POST_NUMBER)
    # when cannot get user posts
    if not posts:
        return JsonResponse({"userid": userid, "username": username, "message": "NOT FOUND"})

    # judge by given posts
    results = evaluate(posts)

    response_data = {"userid": userid, "username": username, "isTroll": results, "message": "SUCCESS"}
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
    resp_json = resp.json()
    userid = resp_json['data']['id']
    return userid


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
    posts = resp.json()['data']
    return posts
