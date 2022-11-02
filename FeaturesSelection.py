import sys
from Main.View.CLIView import CLIView

argv = sys.argv

command_line_interface = CLIView(len(argv), argv, mode="featuresSelction")
command_line_interface.check_if_is_low_variance()
command_line_interface.check_if_is_L1_based_selection()
command_line_interface.check_if_is_sequential_features_selection()
command_line_interface.check_if_is_chi2()
command_line_interface.check_if_is_recursive_tree_features_selection()
# command_line_interface.check_if_is_three_FS()
