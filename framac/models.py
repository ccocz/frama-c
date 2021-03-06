from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField('creation date')
    owner = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    parent_directory = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def list_content(self):
        directory_items = ["directory:begin", self]
        for directory in self.directory_set.all():
            directory_items += directory.list_content()
        for file in self.file_set.all():
            directory_items.append(file)
        directory_items.append("directory:end")
        return directory_items

    def delete_directory(self):
        for directory in self.directory_set.all():
            directory.delete_directory()
        for file in self.file_set.all():
            file.delete_file()
        self.is_available = False
        self.save()


class SectionCategory(models.Model):
    name = models.CharField(max_length=200)


class SectionStatus(models.Model):
    name = models.CharField(max_length=200)


class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login


class StatusData(models.Model):
    data = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class FileSection(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField()
    section_category = models.ForeignKey(SectionCategory, on_delete=models.CASCADE)
    status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
    status_data = models.ForeignKey(StatusData, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField()
    owner = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    parent_directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='framac/files')
    file_sections = models.ManyToManyField(FileSection)  # change
    result = models.TextField()

    def __str__(self):
        return self.name

    def delete_file(self):
        self.is_available = False
        self.save()


class Prover(models.Model):
    name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)


class VC(models.Model):
    name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)