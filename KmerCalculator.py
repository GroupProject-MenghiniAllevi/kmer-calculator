import sys

from Main.View.CLIView import CLIView as cli

arg = sys.argv
command_line = cli(len(arg), arg)
command_line.check_if_is_help()
command_line.check_if_is_DSK()
command_line.check_if_is_gerbil()
command_line.check_if_is_kmc3()
command_line.check_right_command()
