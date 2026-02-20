from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "menuapp/index.html", {"slug": "home"})


def page(request: HttpRequest, slug: str) -> HttpResponse:
    return render(request, "menuapp/index.html", {"slug": slug})

