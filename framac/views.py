from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.utils import timezone

from .forms import UploadFileForm
from .forms import NewDirectoryForm

from .models import Directory
from .models import StatusData
from .models import FileSection
from .models import SectionCategory
from .models import SectionStatus
from .models import File

import os
import subprocess
import re


def index(request):
    root_directory = Directory.objects.get(name='root').__str__()
    # test_source_code = File.objects.get(name="insertion_sort.c").file
    # test_source_code_text = get_actual_source(test_source_code)
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__())}
    # 'test_source': test_source_code_text}
    return render(request, 'framac/index.html', context)


def file_index(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    root_directory = Directory.objects.get(name='root').__str__()
    file_content = get_file_content(file.file)
    file_sections = file.file_sections
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__()),
               'file_content': file_content,
               'file_sections': file_sections,
               'file_id': file_id}
    return render(request, 'framac/index.html', context)


def directory_index(request, directory_id):
    root_directory = Directory.objects.get(name='root').__str__()
    # test_source_code = File.objects.get(name="insertion_sort.c").file
    # test_source_code_text = get_actual_source(test_source_code)
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__()),
               'directory_id': directory_id}
    # 'test_source': test_source_code_text}
    return render(request, 'framac/index.html', context)


def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.delete_file()
    return redirect('framac:index')


def delete_directory(request, directory_id):
    directory = get_object_or_404(Directory, pk=directory_id)
    directory.delete_directory()
    return redirect('framac:index')


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
    nfile = parent_directory.file_set.create(name=name,
                                             description=description,
                                             owner=owner,
                                             is_available=True,
                                             creation_date=timezone.now(),
                                             file=file_)
    cmd = "frama-c -wp -wp-print " + "framac/files/" + name
    result = subprocess.getoutput(cmd)
    parse_file(nfile, result)


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


def get_actual_source(f):
    data = ""
    for chunk in f.chunks():
        data += chunk.decode()
    return data


def parse_file(file, wp_result):
    i = 0
    while i < len(wp_result) and wp_result[i: i + len("----------")] != "----------":
        i += 1
    while i < len(wp_result):
        if is_beginning(wp_result, i):
            section = ""
            while i < len(wp_result) and wp_result[i: i + len("----------")] != "----------":
                section += wp_result[i]
                i += 1
            parse_section_and_add(file, section)
        else:
            i += 1


def parse_section_and_add(file, section):
    category_name = section[len("Goal "):].split("(")[0]
    print("[DEBUG] category_name: " + category_name)
    if SectionCategory.objects.filter(name=category_name).exists():
        section_category = SectionCategory.objects.get(name=category_name)
    else:
        section_category = SectionCategory(name=category_name)
        section_category.save()
    prover_line = re.findall("Prover.*returns.*", section)[0]
    section_status = prover_line.split("returns")[1]
    print("[DEBUG] section_status: " + section_status)
    if SectionStatus.objects.filter(name=section_status).exists():
        section_status_obj = SectionStatus.objects.get(name=section_status)
    else:
        section_status_obj = SectionStatus(name=section_status)
        section_status_obj.save()
    status_data = StatusData(data=section)
    status_data.save()
    file_section = FileSection(creation_date=timezone.now(),
                               section_category=section_category,
                               status=section_status_obj,
                               status_data=status_data)
    file_section.save()
    file.file_sections.add(file_section)


def is_beginning(wp_result, pos):
    return pos + 3 < len(wp_result) and wp_result[pos: pos + len("Goal")] == "Goal"


def get_file_content(f):
    content = ""
    for chunk in f.chunks():
        content += chunk.decode()
    return content