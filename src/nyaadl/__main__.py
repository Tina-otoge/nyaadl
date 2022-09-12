from argparse import ArgumentParser

from . import cli, executor, nyaa


def main():
    parser = ArgumentParser()
    parser.add_argument('search_words', nargs='+')
    parser.add_argument('-s', '--sukebei', action='store_true')
    parser.add_argument('-c', '--command')
    args = parser.parse_args()
    matches = nyaa.lookup(args.search_words, sukebei=args.sukebei)
    target = cli.ask(matches)
    if not target:
        return
    executor.run(target, command=args.command)


if __name__ == '__main__':
    main()
