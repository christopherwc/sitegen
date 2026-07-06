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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt" : "This is an image node"})
    
    
if __name__ == "__main__":
    unittest.main()