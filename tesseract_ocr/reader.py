from argparse import ArgumentParser

from pytesseract import image_to_string


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--invoice", '-i', required=True)
    args = parser.parse_args()

    print(image_to_string(args.invoice))
