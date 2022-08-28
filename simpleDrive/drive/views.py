from email.policy import HTTP
from fileinput import filename
import os, mimetypes
from django.http import HttpResponse
from django.shortcuts import render
from django import forms

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class uploadForm( forms.Form ):
    file = forms.FileField()

class deleteForm( forms.Form ):
    fileName = forms.CharField( max_length="100" )

# Create your views here.
def indexPageHandler( request ):
    context = { "fileList" : [  ] }
    context["fileList"] = os.listdir( os.path.join( BASE_DIR, "files" ) )
    return render( request, 'index.html', context=context )

def uploadPageHandler( request ):
    frm = uploadForm()
    return render( request, 'upload.html', context={ "form" : frm } )

def deletePageHandler( request ):
    frm = deleteForm()
    return render( request, 'delete.html', context={ "form" : frm } )

def downloadFileHandler( request ):
    filePath = os.path.join( BASE_DIR, "files", request.GET.get("fileName") )
    if os.path.exists( filePath ):
        file = open( filePath, 'rb' )
        mime_type = mimetypes.guess_type(filePath)[0]
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=" + request.GET.get( "fileName" )
        return response
    else:
        return render( request, 'message.html', { "type" : "failure", "message" : "Invalid file!" } )

def uploadFileHandler( request ):
    if request.method == "POST":
        frm = uploadForm( request.POST, request.FILES )
        if frm.is_valid() == True:
            file = request.FILES['file']
            filePath = os.path.join( BASE_DIR, "files", file.name )

            if os.path.exists( filePath ):
                return render( request, "messageNav.html", context = { "type" : "Failure", "message" : "File already exists!" } )

            with open( filePath, 'wb+' ) as fl:
                for chunk in file.chunks():
                    fl.write( chunk )
            
            return render( request, "messageNav.html", { "type" : "success", "message" : "File saved successfully" } )
        else:
            return render( request, "messageNav.html", { "type" : "Failure", "message" : "Invalid request!"})
    else:
        return render( request, 'messageNav.html', { "type" : "Failure", "message" : "Invalid Request!"} )

def deleteFileHandler( request ):
    if request.method == "POST":
        frm = deleteForm( request.POST )
        if frm.is_valid() == True:
            filePath = os.path.join( BASE_DIR, "files", frm.cleaned_data["fileName"] )
            if os.path.exists( filePath ):
                os.remove( filePath )
                return render( request, "messageNav.html", context = { "type" : "success", "message" : "File Deleted!" } )
            else:
                return render( request, "messageNav.html", context = { "type" : "failure", "message" : "File Does not Exist!" } )
        else:
            return render( request, "messageNav.html", { "type" : "failure", "message" : "Invalid Request" } )
    else:
        return render( request, "message.html", context = { "message" : "Invalid Request" } )