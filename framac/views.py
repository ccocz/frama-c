from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone

from .forms import UploadFileForm
from .forms import NewDirectoryForm
from .models import Directory

import os


def index(request):
    root_directory = Directory.objects.get(name='root').__str__()
    context = {'root_directory': root_directory, 'range': range(root_directory.__len__())}
    return render(request, 'framac/index.html', context)


def get_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file(form, request.FILES['file'])
            return HttpResponseRedirect('/framac')
    else:
        form = UploadFileForm()
    return render(request, 'framac/add-file.html', {'form': form})


def get_directory(request):
    if request.method == 'POST':
        form = NewDirectoryForm(request.POST)
        if form.is_valid():
            new_directory(form)
            return HttpResponseRedirect('/framac')
    else:
        form = NewDirectoryForm()
    return render(request, 'framac/add-directory.html', {'form': form})


def new_file(form_, file_):
    name = os.path.basename(file_.name)
    owner = form_.cleaned_data['owner']
    description = form_.cleaned_data['description']
    directory = form_.cleaned_data['directory']
    parent_directory = Directory.objects.get(name=directory)
    # should exist
    parent_directory.file_set.create(name=name,
                                     description=description,
                                     owner=owner,
                                     is_available=True,
                                     creation_date=timezone.now())


def new_directory(form_):
    name = form_.cleaned_data['name']
    owner = form_.cleaned_data['owner']
    description = form_.cleaned_data['description']
    directory = form_.cleaned_data['parent_directory']
    parent_directory = Directory.objects.get(name=directory)
    parent_directory.directory_set.create(name=name,
                                          owner=owner,
                                          description=description,
                                          creation_date=timezone.now(),
                                          is_available=True)
