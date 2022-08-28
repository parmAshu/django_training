import json

from django.http import HttpResponse
from django.shortcuts import render

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def homePage( request ):
    context = { "blogList" : [] }
    with open( BASE_DIR / "blogs/blogs.json" ) as file:
        blogs = json.loads( file.read() )
        for blog in blogs:
            del( blog["Content"] )
            blog[ "urlRelative" ] = "/blog?title=" + blog["Title"]
            context["blogList"].append( blog )

    return render( request, 'homePage.html', context=context )

def blogPage( request ):
    blogPath = request.GET.get( "title" )
    context = {}
    with open( BASE_DIR / "blogs/blogs.json" ) as file:
        blogs = json.loads( file.read() )
        for blog in blogs:
            if blog["Title"] == blogPath:
                context = blog
    context["sampleList"] = [ "This", "is", "a", "list" ]
    return render( request, 'blog.html', context = context )