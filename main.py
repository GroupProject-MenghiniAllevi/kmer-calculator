import sys

from Main.View.CLIView import CLIView


def cli():
    arg = sys.argv
    command_line = CLIView(len(arg), arg)
    command_line.check_if_is_help()
    command_line.check_if_is_DSK()
    command_line.check_if_is_gerbil()
    command_line.check_if_is_kmc3()
    command_line.check_if_is_low_variance()
    command_line.check_if_is_L1_based_selection()
    command_line.check_if_is_sequential_features_selection()
    command_line.check_if_is_chi2()
    command_line.check_if_is_recursive_tree_features_selection()
    # command_line.check_if_is_three_FS()

if __name__ == '__main__':
    cli()
