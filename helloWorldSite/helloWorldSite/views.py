from django.http import HttpResponse

def helloWorldResponse( request ):
    response = "<h1>Hello World</h1>"
    return HttpResponse( response )