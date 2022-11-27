from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from rest_framework.decorators import api_view
# Create your views here.

def evaluate(posts):
  return []


@api_view(["GET"])
def judge_user(request, userid):
  # TODO: use userid to get user information, store the latest posts in variable posts: String[]
  if userid == "":
    return JsonResponse({"message": "INVALID USRID"})


  # when cannot get user posts
  if True:
    return JsonResponse({"userid": userid, "message": "NOT FOUND"})

  posts = [] # comment this line 
  
  #judge by given posts
  results = evaluate(posts)

  response_data = {"userid": userid, "isTroll": results, "message": "SUCCESS"}
  return JsonResponse(response_data)

def empty(request):
  return JsonResponse({"message": "This is Troll-Finder Discrimiator!"})