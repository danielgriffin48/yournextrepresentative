from os.path import abspath, dirname, join

from django.test import TestCase
from unittest import skipIf

from sopn_parsing.helpers.text_helpers import clean_text, NoTextInDocumentError
from sopn_parsing.tests import should_skip_pdf_tests

try:
    from sopn_parsing.helpers.pdf_helpers import SOPNDocument
except ImportError:
    pass


class TestSOPNHelpers(TestCase):
    def test_clean_text(self):
        text = "\n C andidates (Namés)"
        self.assertEqual(clean_text(text), "candidates")

    def test_empty_documents(self):
        example_doc_path = abspath(
            join(dirname(__file__), "data/sopn-berkeley-vale.pdf")
        )
        doc = SOPNDocument(
            file=open(example_doc_path, "rb"), source_url="http://example.com"
        )
        doc.heading = {"reason", "2019", "a", "election", "the", "labour"}
        self.assertRaises(NoTextInDocumentError)

    @skipIf(should_skip_pdf_tests(), "Required PDF libs not installed")
    def test_sopn_document(self):
        example_doc_path = abspath(
            join(dirname(__file__), "data/sopn-berkeley-vale.pdf")
        )
        doc = SOPNDocument(
            open(example_doc_path, "rb"), source_url="http://example.com"
        )
        self.assertSetEqual(
            doc.document_heading,
            {
                # Header
                "the",
                "statement",
                "of",
                "persons",
                "nominated",
                "for",
                "stroud",
                "district",
                "berkeley",
                "vale",
                "council",
                "on",
                "thursday",
                "february",
                "28",
                "2019",
                # table headers
                "candidate",
                "name",
                "description",
                "proposer",
                "reason",
                "why",
                "no",
                "longer",
                "(if",
                "any)",
                # candidates
                "simpson",
                "jane",
                "eleanor",
                "liz",
                "ashton",
                "lindsey",
                "simpson",
                "labour",
                "green",
                "party",
                # More words here?
                "election",
                "a",
                "councillor",
                "following",
                "is",
                "as",
            },
        )

        self.assertEqual(len(doc.pages), 1)

    @skipIf(should_skip_pdf_tests(), "Required PDF libs not installed")
    def test_multipage_doc(self):
        example_doc_path = abspath(
            join(dirname(__file__), "data/NI-Assembly-Election-2016.pdf")
        )

        doc = SOPNDocument(
            file=open(example_doc_path, "rb"), source_url="http://example.com"
        )
        self.assertEqual(len(doc.pages), 9)

        for doc_info in doc.match_all_pages():
            self.assertEqual(doc_info[0], doc.pages[0])
            self.assertEqual(doc_info[1], "1,2")
