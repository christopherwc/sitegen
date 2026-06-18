import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
   
    def test_default_url_is_none(self):
        # Tests that url defaults to None if not provided
        node = TextNode("No URL here", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_not_equal_url(self):
        # Tests that nodes with different URLs are not equal
        node = TextNode("Link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_one_url_none_one_url_exists(self):
        # Tests that a node with a URL doesn't match a node without one
        node = TextNode("Link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_empty_string(self):
        # Tests that nodes with matching empty strings are equal
        node = TextNode("", TextType.CODE)
        node2 = TextNode("", TextType.CODE)
        self.assertEqual(node, node2)

    def test_neq_url_is_none_vs_populated(self):
        # Checks edge case where one node has a URL and the other's URL is explicitly None
        node_with_url = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node_with_none = TextNode("Boot.dev", TextType.LINK, None)
        self.assertNotEqual(node_with_url, node_with_none)

    def test_neq_different_text_types(self):
        # Ensures nodes with identical text but different text_type enums are not equal
        node_bold = TextNode("Important Content", TextType.BOLD)
        node_code = TextNode("Important Content", TextType.CODE)
        self.assertNotEqual(node_bold, node_code)

    def test_neq_all_properties_different(self):
        # Tests a total mismatch where text, text_type, and url are all completely different
        node1 = TextNode("Click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Look at this", TextType.IMAGE, "https://boot.dev")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()