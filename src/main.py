
import flet as ft


def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.SafeArea(
            content=ft.Text("Hello, world!", weight=ft.FontWeight.BOLD),
        )
    )


ft.run(main)


