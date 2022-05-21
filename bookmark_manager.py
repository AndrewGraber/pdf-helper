import os
import pikepdf
from prettytable import SINGLE_BORDER
from prettytable.colortable import ColorTable, Themes
from lib.sexytable import SexyTable, ThemeExtra, ExtraThemes

file = None
bookmarks = []
modified = False

def get_file_from_user():
    pdfs = []
    
    table = SexyTable()
    table.title = "Select a File"
    table.field_names = ["Num", "File Name", "Size"]
    for filename in os.listdir('./'):
        if filename.lower().endswith(".pdf"):
            size = os.path.getsize(filename)
            table.add_row([str(len(pdfs)+1), filename, str(size / 1024) + " KB"])
            pdfs.append(filename)

    table.set_style(SINGLE_BORDER)
    table.theme = ExtraThemes.MENU
    table.align = "l"
    print(table)
    selection = input("Choice (1-" + str(len(pdfs)) + "): ")

    return pdfs[int(selection) - 1]
    
def find_existing_bookmarks(pdf):
    bookmarks = []

    with pdf.open_outline() as outline:
        for bookmark in outline.root:
            dictitem = {}
            dictitem['title'] = bookmark.title
            dictitem['page'] = pdf.pages.index(bookmark.action.D[0])
            bookmarks.append(dictitem)
    
    return bookmarks
    
def list_bookmarks():
    table = ColorTable(theme=Themes.OCEAN)
    table.title = "Existing Bookmarks"
    table.set_style(SINGLE_BORDER)
    table.field_names = ["Num", "Bookmark Title", "Page"]
    table.align = "l"
    for n, bookmark in enumerate(bookmarks):
        table.add_row([n, bookmark['title'], bookmark['page']])
    print(table)
    input("Press Enter to continue...")
    
def add_bookmark():
    print("Not Implemented Yet!")
    input("Press Enter to continue...")
    
def modify_bookmark():
    print("Not Implemented Yet!")
    input("Press Enter to continue...")

def remove_bookmark():
    print("Not Implemented Yet!")
    input("Press Enter to continue...")

def program_exit():
    global file
    
    if modified:
        while True:
            print("You have made changes that have not yet been saved! Are you sure you want to exit?")
            response = input("Exit Program? (y/n): ")
            if response.lower() == "y":
                break
            elif response.lower() == "n":
                main_menu()
    file.close()
    exit()
    
menu_actions = [{'name': "Show Bookmarks", 'method': list_bookmarks},
{'name': "Add a Bookmark", 'method': add_bookmark},
{'name': "Modify a Bookmark", 'method': modify_bookmark},
{'name': "Remove a Bookmark", 'method': remove_bookmark},
{'name': "Exit Bookmark Manager", 'method': program_exit}]

def main_menu():
    menu_table = SexyTable(theme=ExtraThemes.MENU)
    menu_table.title = "Bookmark Manager Menu - " + file.filename
    for n, action in enumerate(menu_actions):
        menu_table.add_row([n+1, action['name']])
    menu_table.align = "l"
    print(menu_table.get_string())
    choice = int(input("Select an Option (1-" + str(len(menu_actions)) + "): "))
    
    if choice <= len(menu_actions) and choice > 0:
        menu_actions[choice-1]['method']()
    else:
        print("Please provide a number relating to one of the options above!")

def main():
    global file, bookmarks

    filename = get_file_from_user()
    file = pikepdf.Pdf.open(filename)
    bookmarks = find_existing_bookmarks(file)
    
    while True:
        main_menu()
    
if __name__ == "__main__":
    main()