from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Directory
from .models import File
from .models import User as UserC
from .models import Prover
from .models import VC

from .forms import NewDirectoryForm
from .forms import ProversChooseForm
from .forms import VcChooseForm


# Util methods

def get_empty_directory(name, owner):
    return Directory.objects.create(name=name,
                                    description="user files",
                                    creation_date=timezone.now(),
                                    owner=owner,
                                    is_available=True)


def get_dummy_file(name):
    return File.objects.create(name=name,
                               creation_date=timezone.now(),
                               owner="public",
                               parent_directory=get_empty_directory("usr", "root"))


def get_test_file(self):
    self.client.force_login(User.objects.create(username="tester"))
    test_file_content = open("framac/files/test.c")
    test_file = File.objects.create(name="test_name",
                                    creation_date=timezone.now(),
                                    owner="tester",
                                    parent_directory=get_empty_directory("root", "tester"))
    test_file.file.save("test", test_file_content)
    return test_file


# Tests for models

class DirectoryModelTest(TestCase):

    def test_empty_directory_string(self):
        empty_directory = get_empty_directory("usr", "root")
        self.assertEqual(empty_directory.list_content(), ["directory:begin", empty_directory, "directory:end"])

    def test_directory_with_file_string(self):
        directory = Directory(name="with file",
                              creation_date=timezone.now(),
                              owner='local',
                              is_available=True)
        directory.save()
        directory.file_set.create(name='dummy-file',
                                  creation_date=timezone.now(),
                                  owner="public")
        dummy_file = File.objects.get(name="dummy-file")
        self.assertEqual(directory.list_content(), ["directory:begin", directory, dummy_file, "directory:end"])

    def test_if_deletes_directory(self):
        directory = get_empty_directory("usr", "root")
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

    def test_to_string(self):
        file = get_dummy_file("test-name-str")
        self.assertIs(file.__str__(), "test-name-str")


# Tests for views

class IndexViewTest(TestCase):

    def test_main_page_logged_in(self):
        self.client.force_login(User.objects.create(username="tester"))
        response = self.client.get(reverse("framac:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<!DOCTYPE html>")

    def test_main_page_not_logged_in(self):
        response = self.client.get(reverse("framac:index"))
        self.assertEqual(response.status_code, 302)


class FileIndexViewTest(TestCase):

    def test_valid_file_index(self):
        test_file = get_test_file(self)
        response = self.client.get(reverse("framac:file", kwargs={"file_id": test_file.id}))
        self.assertEqual(response.status_code, 200)

    def test_absent_file_index(self):
        response = self.client.get(reverse("framac:file", kwargs={"file_id": 123}))
        self.assertEqual(response.status_code, 404)

    def test_if_deletes_file(self):
        test_file = get_test_file(self)
        response = self.client.get(reverse("framac:file_delete", kwargs={"file_id": test_file.id}))
        self.assertEqual(response.status_code, 302)

    def test_file_results_section(self):
        test_file = get_test_file(self)
        response = self.client.get(reverse("framac:result", kwargs={"file_id": test_file.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_file(self):
        #self.client.force_login(User.objects.create(username="tester"))
        response = self.client.get(reverse("framac:add-file"))
        test_file = get_test_file(self)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("framac:add-file"), {'file': test_file.file,
                                                                 'description': 'dummy_description',
                                                                 'directory': 'root'})
        self.assertEqual(response.status_code, 302)


class DirectoryIndexViewTest(TestCase):

    def test_valid_directory_index(self):
        self.client.force_login(User.objects.create(username="tester"))
        get_empty_directory("root", "tester")
        response = self.client.get(reverse("framac:directory", kwargs={"directory_id": 123}))
        self.assertEqual(response.status_code, 200)

    def test_if_deletes_directory(self):
        self.client.force_login(User.objects.create(username="tester"))
        directory = get_empty_directory("root", "tester")
        response = self.client.get(reverse("framac:directory_delete", kwargs={"directory_id": directory.id}))
        self.assertEquals(response.status_code, 302)

    def test_get_directory(self):
        self.client.force_login(User.objects.create(username="tester"))
        response = self.client.get(reverse("framac:add-directory"))
        self.assertEqual(response.status_code, 200)
        get_empty_directory("root", "tester")
        response = self.client.post(reverse("framac:add-directory"), {'name': 'test',
                                                                      'description': 'main test',
                                                                      'parent_directory': 'root'})
        self.assertEqual(response.status_code, 302)


class ProverTabViewTest(TestCase):

    def test_get_prover_tab(self):
        self.client.force_login(User.objects.create(username="tester"))
        get_empty_directory("root", "tester")
        Prover.objects.create(name="alt-ergo", is_default=True)
        response = self.client.get(reverse("framac:prover"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("framac:prover"), {'prover': 'alt-ergo'})
        self.assertEqual(response.status_code, 302)


class VcTabViewTest(TestCase):

    def test_get_vc_tab(self):
        self.client.force_login(User.objects.create(username="tester"))
        get_empty_directory("root", "tester")
        VC.objects.create(name="-@invariant", is_default=True)
        response = self.client.get(reverse("framac:vc"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("framac:vc"), {'vc': '-@invariant'})
        self.assertEqual(response.status_code, 302)


# Tests for forms

class NewDirectoryFormTest(TestCase):

    def test_form_with_valid_data(self):
        form_input = {'name': 'tst', 'description': 'testing', 'parent_directory': 'src'}
        form = NewDirectoryForm(form_input)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form_input = {'invalid': 'value'}
        form = NewDirectoryForm(form_input)
        self.assertFalse(form.is_valid())


class ProversChooseFormTest(TestCase):

    def test_with_valid_data(self):
        form_input = {'prover': 'alt-ergo'}
        form = ProversChooseForm(form_input)
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form_input = {'missing': 'alt-ergo'}
        form = ProversChooseForm(form_input)
        self.assertFalse(form.is_valid())


class VcChooseFormTest(TestCase):

    def test_valid_data(self):
        form_data = {'vc': '-@invariant'}
        form = VcChooseForm(form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form_data = {'vc': 'invariant'}
        form = VcChooseForm(form_data)
        self.assertFalse(form.is_valid())
