import os
import sys
from lib.sexytable import SexyTable, ThemeExtra, ExtraThemes

#########################################
# Basic Terminal Manipulation Functions #
#########################################

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def set_cursor(line, column):
    print("\033[{};{}H".format(line, column))

def print_at(line, column, text):
    sys.stdout.write("\x1b7\x1b[{};{}f{}\x1b8".format(line, column, text))
    sys.stdout.flush()
    

class Page:
    def __init__(self, height=None, sections=None):
        self.height = height or os.get_terminal_size().lines
        self.sections = sections or {}

#######################
# SexyTable Functions #
#######################
def make_table(title=None, field_names=[], theme=ExtraThemes.DEFAULT, align=None):
    table = SexyTable()
    
    if title is not None:
        table.title = title
    
    if not field_names == []:
        table.field_names = field_names

    table.theme = theme

    if align is not None:
        table.align = align

    return table

def print_centered_table_at(line, table):
    line_ctr = line
    table_width = table.get_width()
    term_size = os.get_terminal_size()
    column_offset = round((term_size.columns / 2) - (table_width / 2))
    table_str = table.get_string()
    for line in table_str.splitlines():
        set_cursor(line_ctr, column_offset)
        print(line)
        line_ctr += 1
    set_cursor(line_ctr, 0)