from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField('creation date')
    owner = models.CharField(max_length=200)

    # change name
    def __str__(self):
        directory_items = ["directory:begin", self.name]
        for directory in self.directory_set.all():
            directory_items += directory.__str__()
        for file in self.file_set.all():
            directory_items.append(file.__str__())
        directory_items.append("directory:end")
        return directory_items

    is_available = models.BooleanField(default=True)

    parent_directory = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class File(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField()
    owner = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    parent_directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.name


class FileSection(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=400, blank=True)
    creation_date = models.DateTimeField


class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login


class StatusData(models.Model):
    data = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
