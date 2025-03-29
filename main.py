
import flet as ft

import win32com.client

def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.Text("Import was successfull!"),
    )


ft.app(main)


