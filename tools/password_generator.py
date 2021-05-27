from argparse import ArgumentParser
from string import digits, ascii_letters, punctuation
from random import choices, sample


def cleaned(string, denylist):
    for x in denylist:
        string = string.replace(x, "")
    return string


def generate(length, special_count, denylist):
    cleaned(digits + ascii_letters, denylist)
    string = "".join(choices(cleaned(digits + ascii_letters, denylist),
                             k=length - special_count))
    specials = "".join(choices(cleaned(punctuation, denylist), k=special_count))
    return "".join(sample(string + specials, length))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--length", '-l', type=int, default=20)
    parser.add_argument("--special_count", '-s', type=int, default=3)
    parser.add_argument("--denylist", '-d', type=str, default=["\\`/"])

    args = parser.parse_args()

    print(generate(args.length, args.special_count, args.denylist))
