from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Directory
from .forms import UploadFileForm


def index(request):
    root_directory = Directory.objects.get(name='root').__str__()
    context = {'root_directory': root_directory, 'range': range(root_directory.__len__())}
    return render(request, 'framac/index.html', context)


def get_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            for chunk in f.chunks():
                print(chunk)
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'framac/add-file.html', {'form': form})