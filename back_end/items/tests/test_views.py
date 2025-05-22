from django.test import TestCase, Client
from django.contrib.auth.models import User
from items.models import Item
from profiles.models import Profile
from django.urls import reverse
import openpyxl
from io import BytesIO


class ItemsExportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.profile = Profile.objects.create(user=self.user)

        Item.objects.create(name="Item 1", description="Desc 1", author=self.profile)
        Item.objects.create(name="Item 2", description="Desc 2", author=None)

    def test_export_requires_login(self):
        response = self.client.get("/items/export/")
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"You must be logged in", response.content)

    def test_export_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/items/export/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn(
            "attachment; filename=items.xlsx", response["Content-Disposition"]
        )

        wb = openpyxl.load_workbook(filename=BytesIO(response.content))
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))

        self.assertEqual(
            rows[0], ("Index", "Name", "Description", "Author", "Created At")
        )
        self.assertEqual(rows[1][1], "Item 1")
        self.assertEqual(rows[2][1], "Item 2")
