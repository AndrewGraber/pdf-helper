from prettytable.colortable import ColorTable, Theme, RESET_CODE

class ThemeExtra(Theme):
    def __init__(
        self,
        default_color: str = "",
        vertical_color: str = "",
        horizontal_color: str = "",
        junction_color: str = "",
        vertical_char: str = "│",
        horizontal_char: str = "─",
        junction_char: str = "┼",
        top_junction_char: str = "┬",
        bottom_junction_char: str = "┴",
        right_junction_char: str = "┤",
        left_junction_char: str = "├",
        top_right_junction_char: str = "┐",
        top_left_junction_char: str = "┌",
        bottom_right_junction_char: str = "┘",
        bottom_left_junction_char: str = "└"
    ):
        super().__init__(
            default_color,
            vertical_char,
            vertical_color,
            horizontal_char,
            horizontal_color,
            junction_char,
            junction_color
        )
        self.top_junction_char = top_junction_char
        self.bottom_junction_char = bottom_junction_char
        self.right_junction_char = right_junction_char
        self.left_junction_char = left_junction_char
        self.top_right_junction_char = top_right_junction_char
        self.top_left_junction_char = top_left_junction_char
        self.bottom_right_junction_char = bottom_right_junction_char
        self.bottom_left_junction_char = bottom_left_junction_char
        
class ExtraThemes:
    DEFAULT = ThemeExtra()
    MENU = ThemeExtra(
        default_color = "37",
        vertical_color = "33",
        horizontal_color = "33",
        junction_color = "93"
    )

class SexyTable(ColorTable):
    def __init__(self, field_names=None, **kwargs):
        if 'theme' not in kwargs:
            kwargs.set('theme', ExtraThemes.DEFAULT)
        super().__init__(field_names=field_names, **kwargs)
        self.theme = kwargs.get("theme") or ExtraThemes.DEFAULT

    def update_theme(self):
        super().update_theme()
        theme = self._theme
        
        self._top_junction_char = (
            theme.junction_color
            + theme.top_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._bottom_junction_char = (
            theme.junction_color
            + theme.bottom_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._right_junction_char = (
            theme.junction_color
            + theme.right_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._left_junction_char = (
            theme.junction_color
            + theme.left_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._top_right_junction_char = (
            theme.junction_color
            + theme.top_right_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._top_left_junction_char = (
            theme.junction_color
            + theme.top_left_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._bottom_right_junction_char = (
            theme.junction_color
            + theme.bottom_right_junction_char
            + RESET_CODE
            + theme.default_color
        )
        
        self._bottom_left_junction_char = (
            theme.junction_color
            + theme.bottom_left_junction_char
            + RESET_CODE
            + theme.default_color
        )
    
    