
import flet as ft


def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    def handle_click():
        from selenium import webdriver

        driver = webdriver.Chrome()
        driver.get('https://selenium.dev/')
        driver.quit()

    page.add(
        ft.SafeArea(
            content=ft.TextButton("Launch Chrome Browser", on_click=handle_click),
        )
    )


ft.run(main)


