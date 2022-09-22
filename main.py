import sys

from it.unicam.cs.groupproject.kmer.CLIView import CLIView


def cli():
    print("hi")
    arg = sys.argv
    command_line = CLIView(len(arg), arg)
    command_line.check_if_is_help()
    command_line.check_if_is_DSK()


if __name__ == '__main__':
    cli()
