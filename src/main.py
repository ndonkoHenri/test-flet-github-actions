import flet_webview as fwv

import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=fwv.WebView(
                url="https://flet.dev",
                on_page_started=lambda _: print("Page started"),
                on_page_ended=lambda _: print("Page ended"),
                on_web_resource_error=lambda e: print("WebView error:", e.data),
                expand=True,
            )
        )
    )


ft.run(main)