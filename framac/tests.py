from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Directory
from .models import File
from .models import User as UserC

from .forms import NewDirectoryForm

def get_empty_directory():
    return Directory.objects.create(name="usr",
                                    description="user files",
                                    creation_date=timezone.now(),
                                    owner="root",
                                    is_available=True)


def get_dummy_file(name):
    return File.objects.create(name=name,
                               creation_date=timezone.now(),
                               owner="public",
                               parent_directory=get_empty_directory())


class DirectoryModelTest(TestCase):

    def test_empty_directory_string(self):
        empty_directory = get_empty_directory()
        self.assertEqual(empty_directory.list_content(), ["directory:begin", empty_directory, "directory:end"])

    def test_directory_with_file_string(self):
        directory = Directory(name="with file",
                              creation_date=timezone.now(),
                              owner='local',
                              is_available=True)
        # file = File.objects.get(name="sum.c")
        # print(file.creation_date)
        # print(directory.list_content())
        # self.assertEqual(directory.list_content(), ["directory:begin", directory, file, "directory:end"])

    def test_if_deletes_directory(self):
        directory = get_empty_directory()
        directory.delete_directory()
        self.assertFalse(directory.is_available)


class UserModelTest(TestCase):

    def test_user_login_string(self):
        user = UserC.objects.create(name="user_name",
                                    login="dummy-login",
                                    password="dummy-password")
        self.assertIs(user.__str__(), "dummy-login")


class FileModelTest(TestCase):

    def test_if_deletes_file(self):
        file_tbd = get_dummy_file("dummy-name")
        file_tbd.delete_file()
        self.assertFalse(file_tbd.is_available)

    def test_file_name_string(self):
        file = get_dummy_file("test-name")
        self.assertIs(file.name, "test-name")


class IndexViewTest(TestCase):

    def test_main_page_logged_in(self):
        self.client.force_login(User.objects.create(username="tester"))
        response = self.client.get(reverse("framac:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<!DOCTYPE html>")

    def test_main_page_not_logged_in(self):
        response = self.client.get(reverse("framac:index"))
        self.assertEqual(response.status_code, 302)


class NewDirectoryFormTest(TestCase):

    def test_form(self):
        form_input = {'name': 'tst', 'description':'testing', 'parent_directory':'src'}
        form = NewDirectoryForm(data=form_input)
        self.assertTrue(form.is_valid())


