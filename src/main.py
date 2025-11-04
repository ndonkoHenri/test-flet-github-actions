
import flet as ft
import flet_ads
import flet_audio
import flet_audio_recorder
import flet_charts
import flet_datatable2
import flet_flashlight
import flet_geolocator
import flet_lottie
import flet_map
import flet_permission_handler
import flet_rive
import flet_video
import flet_webview


def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    page.add(
        ft.SafeArea(
            content=ft.Text("Hello, world!", weight=ft.FontWeight.BOLD),
        )
    )


ft.run(main)


