import unittest

from split_nodes import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
    # ==========================================
    # Tests for extract_markdown_images
    # ==========================================

    def test_image_standard(self):
        """Should extract a single standard image markdown."""
        text = "Check this out: ![alt text](https://example.com/image.png)"
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_multiple(self):
        """Should extract multiple images from the same text string."""
        text = "![one](img1.jpg) some text in between ![two](img2.jpg)"
        expected = [("one", "img1.jpg"), ("two", "img2.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_empty_alt_text(self):
        """Should handle an image with no alt text."""
        text = "![](https://example.com/blank.png)"
        expected = [("", "https://example.com/blank.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_ignores_regular_links(self):
        """Should completely ignore regular links lacking the '!' prefix."""
        text = "This is a [link](https://google.com), not an image."
        self.assertEqual(extract_markdown_images(text), [])

    # ==========================================
    # Tests for extract_markdown_links
    # ==========================================

    def test_link_standard(self):
        """Should extract a single standard link markdown."""
        text = "Click here: [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_multiple(self):
        """Should extract multiple links from the same text string."""
        text = "[GitHub](https://github.com) and [GitLab](https://gitlab.com)"
        expected = [
            ("GitHub", "https://github.com"),
            ("GitLab", "https://gitlab.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_ignores_images(self):
        """Should look behind for '!' and ignore image markdown syntax entirely."""
        text = "An image ![alt](img.png) and a link [anchor](url.com)"
        expected = [("anchor", "url.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    # ==========================================
    # Edge Cases & Boundary Conditions
    # ==========================================

    def test_empty_string(self):
        """Both functions should gracefully return empty lists for empty strings."""
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_malformed_markdown(self):
        """Should not extract broken, unclosed, or nested brackets."""
        broken_texts = [
            "[link(url.com)",
            "link](url.com)",
            "[link]url.com)",
            "![alt](url.com",
            "[link](url with (nested) parens)",  # Current regex ignores this due to ([^\(\)]*)
        ]
        for text in broken_texts:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_images(text), [])
                self.assertEqual(extract_markdown_links(text), [])

if __name__ == "__main__":
    unittest.main()
