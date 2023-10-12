# from django.shortcuts import render
from django.http import HttpResponse
from urllib import request


def url1(resuest):
    return HttpResponse('Answer 1')


def url2(resuest):
    return HttpResponse('Answer 2')


def url3(resuest):
    return HttpResponse(request)