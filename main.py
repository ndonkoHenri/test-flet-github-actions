import os
from datetime import datetime
import flet as ft

# constants
FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
COUNTER_FILE_PATH = os.path.join(FLET_APP_STORAGE_DATA, "counter.txt")
FLET_APP_CONSOLE = os.getenv("FLET_APP_CONSOLE")


class Counter(ft.Text):
    def __init__(self, storage_path=COUNTER_FILE_PATH):
        super().__init__(theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.storage_path = storage_path
        self.count = self.__read_from_storage()

    def increment(self):
        """Increment the counter, store the new value, and return it."""
        self.count += 1
        self.update()
        self.__write_to_storage()

    def before_update(self):
        super().before_update()
        self.value = f"Button tapped {self.count} time{'' if self.count == 1 else 's'}"

    def __log(self, action: str, value: int = None):
        """Log executed action."""
        if value is None:
            value = self.count
        print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - {action} = {value}")

    def __read_from_storage(self):
        """Read counter value. If an error occurs, use 0."""
        try:
            with open(self.storage_path, "r") as f:
                value = int(f.read().strip())
        except (FileNotFoundError, ValueError): 
            # file does not exist or int parsing failed
            value = 0

        self.__log("READ", value)
        return value

    def __write_to_storage(self):
        """Write current counter value to storage."""
        with open(self.storage_path, "w") as f:
            f.write(str(self.count))
        self.__log("WRITE")


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_logs(e: ft.ControlEvent):
        if FLET_APP_CONSOLE is not None:
            with open(FLET_APP_CONSOLE, "r") as f:
                dlg = ft.AlertDialog(
                    title=ft.Text("App Logs"),
                    content=ft.Text(f.read()),
                    scrollable=True,
                )
                page.open(dlg)

    counter = Counter()
    page.appbar = ft.AppBar(
        title=ft.Text("Storage Playground", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        adaptive=True,
        actions=[
            ft.IconButton(
                icon=ft.Icons.REMOVE_RED_EYE,
                tooltip="Show logs",
                visible=FLET_APP_CONSOLE is not None,
                on_click=show_logs,
            ),
        ],
    )
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Increment Counter",
        foreground_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda e: counter.increment(),
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT

    page.add(ft.SafeArea(counter))


ft.app(main)
