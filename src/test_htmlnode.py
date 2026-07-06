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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None,"Hello, world!")
        self.assertEqual(node.to_html(),"Hello, world!")
    
    def test_leaf_all_params(self):
        node = LeafNode("a","Hello, world!",{"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com" target="_blank">Hello, world!</a>')
    
    def test_leaf_no_value(self):
        node = LeafNode(None,None,None) 
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()