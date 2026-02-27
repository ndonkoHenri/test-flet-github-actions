
import flet as ft
import sqlalchemy

def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.SafeArea(
            content=ft.Text(f"Hello, SqlAlchemy v{sqlalchemy.__version__}!"),
        )
    )


ft.run(main)


