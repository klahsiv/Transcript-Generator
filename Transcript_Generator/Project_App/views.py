from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import csv

# Create your views here.

class MyCustomStorage(FileSystemStorage):
    def get_available_name(self, name, max_length = None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(MyCustomStorage, self)._save(name, content)

def home(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = MyCustomStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'Project_App/home.html', {'file_url': file_url})
    return render(request, "Project_App/home.html")

def save_range(request):
    if request.GET.get("start"):
        message = 'Starting Roll No.: %r' % request.GET['start']
    else:
        message = 'You submitted nothing!'
    
    if request.GET.get('end'):
        message += ' <br> Ending Roll No: %r' % request.GET['end']
    else:
        message += ' <br> You submitted nothing!'
    
    if os.path.exists("Project_App/range.csv"):
        os.remove("Project_App/range.csv")
    
    with open("Project_App/range.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([request.GET["start"], request.GET["end"]])
        file.close()
    return HttpResponse(message)

from .generate_all import *
def all_transcript(request):
    print("Do something Here")
    generate_all()
    return HttpResponse("Succesfull")

from .generate_range import *
def range_transcript(request):
    print("Range Generation here")
    generate_range()
    return HttpResponse("Succesfull")