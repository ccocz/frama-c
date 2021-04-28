from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    owner = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400, required=False)
    directory = forms.CharField(max_length=200)


class NewDirectoryForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=400, required=False)
    owner = forms.CharField(max_length=60)
    parent_directory = forms.CharField(max_length=200)
