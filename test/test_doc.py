import datetime
import os
import unittest

from odml import Document
from odml.doc import BaseDocument
from odml.dtypes import FORMAT_DATE


class TestSection(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_attributes(self):
        author = "HPL"
        version = "4.8.15"
        doc = Document(author=author, version=version)

        self.assertEqual(doc.author, author)
        self.assertEqual(doc.version, version)

        doc.author = ""
        doc.version = ""
        self.assertIsNone(doc.author)
        self.assertIsNone(doc.version)

        doc.author = author
        doc.version = version
        self.assertEqual(doc.author, author)
        self.assertEqual(doc.version, version)

    def test_id(self):
        doc = Document()
        self.assertIsNotNone(doc.id)

        doc = Document("D", id="79b613eb-a256-46bf-84f6-207df465b8f7")
        self.assertEqual(doc.id, "79b613eb-a256-46bf-84f6-207df465b8f7")

        doc = Document("D", id="id")
        self.assertNotEqual(doc.id, "id")

        # Make sure id cannot be reset programmatically.
        with self.assertRaises(AttributeError):
            doc.id = "someId"

    def test_new_id(self):
        doc = Document()
        old_id = doc.id

        # Test assign new generated id.
        doc.new_id()
        self.assertNotEqual(old_id, doc.id)

        # Test assign new custom id.
        old_id = doc.id
        doc.new_id("79b613eb-a256-46bf-84f6-207df465b8f7")
        self.assertNotEqual(old_id, doc.id)
        self.assertEqual("79b613eb-a256-46bf-84f6-207df465b8f7", doc.id)

        # Test invalid custom id exception.
        with self.assertRaises(ValueError):
            doc.new_id("crash and burn")

    def test_date(self):
        datestring = "2000-01-02"
        doc = Document(date=datestring)

        self.assertIsInstance(doc.date, datetime.date)
        self.assertEqual(doc.date,
                         datetime.datetime.strptime(datestring, FORMAT_DATE).date())

        doc.date = None
        self.assertIsNone(doc.date)

        doc.date = datestring
        self.assertIsInstance(doc.date, datetime.date)
        self.assertEqual(doc.date,
                         datetime.datetime.strptime(datestring, FORMAT_DATE).date())

        doc.date = []
        self.assertIsNone(doc.date)
        doc.date = {}
        self.assertIsNone(doc.date)
        doc.date = ()
        self.assertIsNone(doc.date)
        doc.date = ""
        self.assertIsNone(doc.date)

        with self.assertRaises(ValueError):
            doc.date = "some format"

    def test_get_terminology_equivalent(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_file = os.path.join(dir_path, "resources",
                                           "local_repository_file_v1.1.xml")
        local_url = "file://%s" % repo_file

        doc = Document(repository=local_url)

        teq = doc.get_terminology_equivalent()
        self.assertIsInstance(teq, BaseDocument)
        self.assertEqual(len(teq), 1)
        self.assertEqual(teq.sections[0].name, "Repository test")

        doc.repository = None
        self.assertIsNone(doc.get_terminology_equivalent())
