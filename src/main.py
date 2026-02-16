
import flet as ft


def main(page: ft.Page):
    page.appbar = ft.AppBar(title="Playground", center_title=True)
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.SafeArea(
            content=ft.Text("Hello, world!", weight=ft.FontWeight.BOLD, size=25),
        )
    )


ft.run(main)


