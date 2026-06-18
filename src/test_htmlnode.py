"""
Unit tests for the HTMLNode class, focusing primarily on attribute serialization.
"""

import unittest
from htmlnode import HTMLNode  # Assumes HTMLNode is in src/htmlnode.py or similar


class TestHTMLNode(unittest.TestCase):
    """Test suite for validating HTMLNode functionality."""

    def test_props_to_html_with_multiple_props(self):
        """Test that a dictionary of multiple properties formats correctly into an HTML string."""
        node = HTMLNode(
            tag="a",
            value="Click here",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_none_props(self):
        """Test that props_to_html returns an empty string when props is None."""
        node = HTMLNode(tag="p", value="Hello, world!", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_dict(self):
        """Test that props_to_html returns an empty string when props is an empty dictionary."""
        node = HTMLNode(tag="h1", value="Welcome", props={})
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()