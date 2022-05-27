import os
import sys
from lib.sexytable import SexyTable, ThemeExtra, ExtraThemes

#########################################
# Basic Terminal Manipulation Functions #
#########################################

ANSI_RESET = "\x1b[0m"

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def set_cursor(line, column):
    print("\033[{};{}H".format(line, column))

def print_at(line, column, text):
    sys.stdout.write("\x1b7\x1b[{};{}f{}\x1b8".format(line+1, column+1, text))
    sys.stdout.flush()
    
def ansi_escape_color(color):
    if color.endswith("m"):
        return color
    else:
        return "\x1b[" + color + "m"
    
##############
# Page Class #
##############

class Page:
    def __init__(self, height=None, border=None, padding=1):
        self.height = height or os.get_terminal_size().lines
        self.width = os.get_terminal_size().columns
        self.padding = padding
        self.line_cursor = 1 + self.padding
        self.column_cursor = 1 + self.padding
        
        self.border = {}
        try:
            self.border['vchar'] = border['vchar']
        except:
            self.border['vchar'] = "│"
            
        try:
            self.border['hchar'] = border['hchar']
        except:
            self.border['hchar'] = "─"
            
        try:
            self.border['jchar'] = border['jchar']
        except:
            self.border['jchar'] = "┼"
            
        try:
            self.border['colors'] = border['colors']
        except:
            self.border['colors'] = ["37"]
            
        try:
            self.border['jcolor'] = border['jcolor']
        except:
            self.border['jcolor'] = "97"
        
        self.border['jcolor'] = ansi_escape_color(self.border['jcolor'])
        for index, color in enumerate(self.border['colors']):
            self.border['colors'][index] = ansi_escape_color(color)
            
    def update_size(self):
        term_size = os.get_terminal_size()
        if self.height > term_size.lines:
            self.height = term_size.lines
        if self.width > term_size.columns:
            self.width = term_size.columns
            
    def draw_hrule(self, line):
        txt = self.border['jcolor'] + self.border['jchar']
        for i in range(self.width-2):
            txt += self.border['colors'][i % len(self.border['colors'])] + self.border['hchar']
        txt += self.border['jcolor'] + self.border['jchar'] + ANSI_RESET
        print_at(line, 0, txt)
        
    def draw_sides(self):
        for i in range(self.height - 2):
            txt = self.border['colors'][i % len(self.border['colors'])] + self.border['vchar'] + ANSI_RESET
            print_at(i+1, 0, txt)
            print_at(i+1, self.width-1, txt)
            
    def draw_border(self):
        self.draw_hrule(0)
        self.draw_sides()
        self.draw_hrule(self.height-1)
        
    def get_content(self):
        return "This is the default page text!\nCreate your own implementation of get_content()\nto override this with your content!"
        
    def draw_content(self):
        txt = self.get_content()
        
        txt_lines = txt.splitlines()
        for line in txt_lines:
            print_at(self.line_cursor, self.column_cursor, line)
            self.line_cursor += 1
            if self.line_cursor > self.height - 1 - self.padding:
                break
                
        if self.line_cursor < self.height - 2:
            self.line_cursor += 1
            if self.line_cursor > self.height - 2:
                self.line_cursor = self.height - 2
            set_cursor(self.line_cursor, self.column_cursor)
        else:
            set_cursor(self.height - 1, 0)
            
    def get_input(self):
        input("Press Enter to Continue...")
        
    def draw(self):
        clear_screen()
        self.update_size()
        self.draw_border()
        self.draw_content()
        self.get_input()

#######################
# SexyTable Functions #
#######################
def make_table(title=None, field_names=[], theme=ExtraThemes.DEFAULT, align=None, bright_title=False, **kwargs):
    table = SexyTable(bright_title=bright_title, **kwargs)
    
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