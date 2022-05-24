import os
import pikepdf
from lib.sexytable import SexyTable, ExtraThemes
import display_helper as display

file = None
bookmarks = []
modified = False

def get_file_from_user():
    pdfs = []

    suffixes = ["B", "KiB", "MiB", "GiB"]
    suffix_cursor = 0
    
    table = display.make_table(
        title = "Select a File",
        field_names = ["Num", "File Name", "Size"],
        theme = ExtraThemes.MENU,
        align = "l"
    )

    for filename in os.listdir('./'):
        if filename.lower().endswith(".pdf"):
            size = os.path.getsize(filename)
            while size >= 1024:
                size = size / 1024
                suffix_cursor += 1
                if suffix_cursor == len(suffixes)-1:
                    break

            table.add_row([str(len(pdfs)+1), filename, '{0:.2f}'.format(size) + " " + suffixes[suffix_cursor]])
            pdfs.append(filename)

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
    display.clear_screen()

    menu_table = display.make_table(
        title = "Bookmark Manager Menu - " + file.filename,
        theme = ExtraThemes.MENU,
        align = "l"
    )

    menu_table.header = False

    for n, action in enumerate(menu_actions):
        menu_table.add_row([n+1, action['name']])

    throwaway = menu_table.get_string()
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