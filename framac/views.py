from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.utils import timezone

from .forms import UploadFileForm
from .forms import NewDirectoryForm
from .forms import ProversChooseForm
from .forms import VcChooseForm

from .models import Directory
from .models import StatusData
from .models import FileSection
from .models import SectionCategory
from .models import SectionStatus
from .models import File
from .models import Prover
from .models import VC

import os
import subprocess
import re


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/framac/users/login')
    if not Directory.objects.filter(name='root', owner=request.user.username).exists():
        root = Directory(name='root',
                         owner=request.user.username,
                         description="root directory of the user",
                         creation_date=timezone.now(),
                         is_available=True)
        root.save()
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__())}
    return render(request, 'framac/index.html', context)


def file_index(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    file_content = get_file_content(file.file)
    file_sections = file.file_sections
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__()),
               'file_content': file_content,
               'file_sections': file_sections,
               'file_id': file_id}
    return render(request, 'framac/index.html', context)


def directory_index(request, directory_id):
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__()),
               'directory_id': directory_id}
    return render(request, 'framac/index.html', context)


def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.delete_file()
    return redirect('framac:index')


def delete_directory(request, directory_id):
    directory = get_object_or_404(Directory, pk=directory_id)
    directory.delete_directory()
    return redirect('framac:index')


def prover_tab(request):
    if request.method == 'POST':
        form = ProversChooseForm(request.POST)
        if form.is_valid():
            change_prover(form.cleaned_data['prover'])
            return HttpResponseRedirect('/framac')
    else:
        form = ProversChooseForm()
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    current_prover = Prover.objects.get(is_default=True)
    return render(request, 'framac/index.html', {'form': form,
                                                 'root_directory': root_directory,
                                                 'range': range(root_directory.__len__()),
                                                 'url': "framac:prover",
                                                 'data': "current prover: " + current_prover.name})


def change_prover(prover):
    current = Prover.objects.get(is_default=True)
    current.is_default = False
    current.save()
    new_prover = Prover.objects.get(name=prover)
    new_prover.is_default = True
    new_prover.save()


def vc_tab(request):
    if request.method == 'POST':
        form = VcChooseForm(request.POST)
        if form.is_valid():
            change_vc(form.cleaned_data['vc'])
            return HttpResponseRedirect('/framac')
    else:
        form = VcChooseForm()
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    current_vc = VC.objects.get(is_default=True)
    return render(request, 'framac/index.html', {'form': form,
                                                 'root_directory': root_directory,
                                                 'range': range(root_directory.__len__()),
                                                 'url': "framac:vc",
                                                 'data': "current vc: " + current_vc.name})


def change_vc(vc):
    current = VC.objects.get(is_default=True)
    current.is_default = False
    current.save()
    new_vc = VC.objects.get(name=vc)
    new_vc.is_default = True
    new_vc.save()


def result(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    root_directory = Directory.objects.get(name='root', owner=request.user.username).__str__()
    file_content = get_file_content(file.file)
    file_sections = file.file_sections
    context = {'root_directory': root_directory,
               'range': range(root_directory.__len__()),
               'file_content': file_content,
               'file_sections': file_sections,
               'file_id': file_id,
               'data': file.result}
    return render(request, 'framac/index.html', context)


def get_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file(request.user.username, form, request.FILES['file'])
            return HttpResponseRedirect('/framac')
    else:
        form = UploadFileForm()
    return render(request, 'framac/add-file.html', {'form': form})


def get_directory(request):
    if request.method == 'POST':
        form = NewDirectoryForm(request.POST)
        if form.is_valid():
            new_directory(request.user.username, form)
            return HttpResponseRedirect('/framac')
    else:
        form = NewDirectoryForm()
    return render(request, 'framac/add-directory.html', {'form': form})


def new_file(user, form_, file_):
    name = os.path.basename(file_.name)
    #owner = form_.cleaned_data['owner']
    owner = user
    description = form_.cleaned_data['description']
    directory = form_.cleaned_data['directory']
    parent_directory = Directory.objects.get(name=directory, owner=user)
    # should exist
    nfile = parent_directory.file_set.create(name=name,
                                             description=description,
                                             owner=owner,
                                             is_available=True,
                                             creation_date=timezone.now(),
                                             file=file_)
    cmd = "frama-c -wp -wp-log=\"r:result.txt\"  " + "framac/files/" + name
    os.system(cmd)
    cmd = "cat result.txt"
    result_file = subprocess.getoutput(cmd)
    nfile.result = result_file
    nfile.save()
    cmd = "frama-c -wp -wp-print " + "framac/files/" + name
    result_file = subprocess.getoutput(cmd)
    parse_file(nfile, result_file)


def reprove(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    name = os.path.basename(file.name)
    cmd = "frama-c -wp -wp-log=\"r:result.txt\"  " + "framac/files/" + name
    os.system(cmd)
    cmd = "cat result.txt"
    new_result = subprocess.getoutput(cmd)
    file.result = new_result
    prover = get_object_or_404(Prover, is_default=True).name
    vc = get_object_or_404(VC, is_default=True).name
    cmd = "frama-c -wp -wp-prover " + prover + " -wp-prop=\" " + vc + "\" -wp-rte -wp-print " + "framac/files/" + name
    new_result = subprocess.getoutput(cmd)
    for section in file.file_sections.all():
        section.delete()
    file.file_sections.clear()
    parse_file(file, new_result)
    return file_index(request, file_id)


def new_directory(user, form_):
    name = form_.cleaned_data['name']
    #owner = form_.cleaned_data['owner']
    owner = user
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
    #print("[DEBUG] category_name: " + category_name)
    if SectionCategory.objects.filter(name=category_name).exists():
        section_category = SectionCategory.objects.get(name=category_name)
    else:
        section_category = SectionCategory(name=category_name)
        section_category.save()
    prover_line = re.findall("Prover.*returns.*", section)[0]
    section_status = prover_line.split("returns")[1]
    #print("[DEBUG] section_status: " + section_status)
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
