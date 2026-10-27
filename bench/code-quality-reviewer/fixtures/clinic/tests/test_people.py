import unittest

from clinic.people import email, names, phone


class PeopleTest(unittest.TestCase):
    def test_names(self):
        self.assertEqual(names.display_name(" Ada ", "Quill"), "Ada Quill")
        self.assertEqual(names.display_name("", "Quill"), "Quill")

    def test_phone(self):
        self.assertEqual(phone.normalize("+44 (0)20 7946 0018"), "+442079460018")

    def test_email(self):
        self.assertTrue(email.looks_valid("ada@example.com"))
        self.assertFalse(email.looks_valid("ada@example"))
        self.assertFalse(email.looks_valid("@example.com"))
