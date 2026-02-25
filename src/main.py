
import flet as ft
import flet_audio as fta 

def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.SafeArea(
            content=ft.TextButton("Hello World!"),
        )
    )


ft.run(main)


