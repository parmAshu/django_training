import os, mimetypes
from django import forms
from django.http import request, HttpResponse, FileResponse
from django.shortcuts import render

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class uploadForm( forms.Form ):
    file = forms.FileField()

class deleteForm( forms.Form ):
    fileName = forms.CharField( label="File Name" )

def indexHandler( request ):
    files = os.listdir( os.path.join( BASE_DIR, 'files' ) )
    context = { "fileList" : files }
    return render( request, 'index.html', context=context )

def uploadPageHandler( request ):
    frm = uploadForm()
    return render( request, "upload.html", context={ "form" : frm } )

def deletePageHandler( request ):
    frm = deleteForm()
    return render( request, "delete.html", context={ "form" : frm } )

def downloadFileHandler( request ):
    filePath = os.path.join( BASE_DIR, "files", request.GET.get("fileName") )
    if os.path.exists( filePath ):
        file = open( filePath, "rb" )
        mime_type, _ = mimetypes.guess_type(filePath)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=" + request.GET.get( "fileName" )
        return response
    else:
        return render( request, 'message.html', {"message" : "File does not exist"} )

def uploadFileHandler( request ):
    frm = uploadForm( request.POST, request.FILES )
    if frm.is_valid() == True:
        file = request.FILES["file"]
        filePath = os.path.join( BASE_DIR, "files", file.name )

        if os.path.exists( filePath ):
            return render( request, "message.html", context = { "message" : "File already exists!" } )

        with open( filePath, 'wb+' ) as fl:
            for chunk in file.chunks():
                fl.write( chunk )

        return render( request, "message.html", context = { "message" : "File uploaded!" } )
    else:
        return render( request, "message.html", context = { "message" : "Invalid Request" } )

def deleteFileHandler( request ):
    frm = deleteForm( request.POST )
    if request.method == "POST" and frm.is_valid() == True:
        filePath = os.path.join( BASE_DIR, "files", frm.cleaned_data["fileName"] )
        if os.path.exists( filePath ):
            os.remove( filePath )
            return render( request, "message.html", context = { "message" : "File Deleted!" } )
        else:
            return render( request, "message.html", context = { "message" : "File Does not Exist!" } )
    else:
        return render( request, "message.html", context = { "message" : "Invalid Request" } )
    
