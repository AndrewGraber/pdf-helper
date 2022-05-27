import os
import display_helper as display
from display_helper import Page
from lib.sexytable import ExtraThemes

class MainMenuPage(Page):
    def __init__(self, file):
        super().__init__(border = {'colors': ["33", "93"], 'jcolor': "93"})
        self.file = file
        self.modified = False
        
        self.menu_actions = [
            {'name': "Show Bookmarks", 'method': self.list_bookmarks},
            {'name': "Add a Bookmark", 'method': self.add_bookmark},
            {'name': "Modify a Bookmark", 'method': self.modify_bookmark},
            {'name': "Remove a Bookmark", 'method': self.remove_bookmark},
            {'name': "Exit Bookmark Manager", 'method': self.program_exit}
        ]
    
    def get_content(self):
        text = ""
        
        menu_table = display.make_table(
            title = "Bookmark Manager Menu - " + self.file.filename,
            header = False,
            theme = ExtraThemes.MENU,
            align = "l",
            max_table_width = os.get_terminal_size().columns - 4
        )

        menu_table.header = False

        for n, action in enumerate(self.menu_actions):
            menu_table.add_row([n+1, action['name']])

        #throwaway = menu_table.get_string()
        text += menu_table.get_string()
        return text
            
    def get_input(self):
        text = "Select an Option (1-" + str(len(self.menu_actions)) + "): "
        display.print_at(self.line_cursor, self.column_cursor, text)
        choice = int(input())
        display.set_cursor(self.line_cursor, self.column_cursor)
        
        if choice <= len(self.menu_actions) and choice > 0:
            self.menu_actions[choice-1]['method']()
        else:
            print("Please provide a number relating to one of the options above!")
            
    def list_bookmarks(self):
        display.clear_screen()

        table = display.make_table(
            title = "Existing Bookmarks",
            field_names = ["Num", "Bookmark Title", "Page"],
            align = "l"
        )

        for n, bookmark in enumerate(bookmarks):
            table.add_row([n, bookmark['title'], bookmark['page']])
        
        display.print_centered_table_at(2, table)
        input("Press Enter to continue...")
        
    def add_bookmark(self):
        print("Not Implemented Yet!")
        input("Press Enter to continue...")
        
    def modify_bookmark(self):
        print("Not Implemented Yet!")
        input("Press Enter to continue...")

    def remove_bookmark(self):
        print("Not Implemented Yet!")
        input("Press Enter to continue...")

    def program_exit(self):
        if self.modified:
            while True:
                print("You have made changes that have not yet been saved! Are you sure you want to exit?")
                response = input("Exit Program? (y/n): ")
                if response.lower() == "y":
                    break
                elif response.lower() == "n":
                    self.draw()
        self.file.close()
        exit()