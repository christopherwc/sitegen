import sys
from textnode import TextType,TextNode

def main(args):
    temp = TextNode(text="Test",text_type=TextType.BOLD)
    print(temp)

if __name__ == "__main__":
    # pass command-line arguments (excluding the script name itself)
    sys.exit(main(sys.argv[1:]))