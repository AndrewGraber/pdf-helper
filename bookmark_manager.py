import os
import pikepdf
from lib.sexytable import SexyTable, ExtraThemes
import display_helper as display

from display_pages.main_menu import MainMenuPage

file = None
bookmarks = []

def get_file_from_user():
    pdfs = []

    suffixes = ["B", "KiB", "MiB", "GiB"]
    suffix_cursor = 0

    table = display.make_table(
        title = "Select a File",
        field_names = ["Num", "File Name", "Size"],
        theme = ExtraThemes.FILE_PICKER,
        align = "l",
        bright_title = True
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

def main():
    global file, bookmarks

    filename = get_file_from_user()
    file = pikepdf.Pdf.open(filename)
    bookmarks = find_existing_bookmarks(file)
    
    menu_page = MainMenuPage(file)
    while True:
        menu_page.draw()
    
if __name__ == "__main__":
    main()