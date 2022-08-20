from django import forms
from django.shortcuts import render
from django.http import HttpResponse

class userForm( forms.Form ):
    #template_name = "formBlock.html"
    name = forms.CharField( label = "name", max_length=50 )
    email = forms.EmailField()

# Create your views here.
def homePageHandler( request ):
    frm = userForm()
    return render( request, "userHomePage.html", { "form" : frm } )

def helloPageHandler( request ):
    context = { "User" : "No Username", "email" : "No email" }
    if request.method == "POST":
        frm = userForm( request.POST )
        if frm.is_valid() == True:
            context["User"] = frm.cleaned_data["name"]
            context["email"] = frm.cleaned_data["email"]
            return render( request, "helloPage.html", context=context )
        else:
            return HttpResponse( "Invalid Data")
    else:
        return HttpResponse( "Invalid Request")
